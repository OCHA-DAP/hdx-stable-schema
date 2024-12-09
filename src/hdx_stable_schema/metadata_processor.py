#!/usr/bin/env python
# encoding: utf-8

import json
from random import randrange

import requests

from pathlib import Path

from hxl.input import hash_row

from hdx_stable_schema.utilities import print_table_from_list_of_dicts

CKAN_API_ROOT_URL = "https://data.humdata.org/api/action/"

SHAPE_INFO_DATA_TYPE_LOOKUP = {
    "character varying": "string",
    "integer": "integer",
    "bigint": "integer",
    "numeric": "float",
    "USER-DEFINED": "user-defined",
    "timestamp with time zone": "timestamp",
    "date": "date",
}


def read_metadata_from_file(file_path: str | Path) -> dict:
    metadata_dict = {}

    with open(file_path, encoding="utf-8") as metadata_file:
        metadata_dict = json.load(metadata_file)

    # We do this because we want to handle package_search and package_show results
    # transparently and they have slightly different formats. It assumes there is just
    # one dataset record in a package_search response

    if "results" in metadata_dict["result"].keys():
        assert len(metadata_dict["result"]["results"]) == 1
        metadata_dict["result"] = metadata_dict["result"]["results"][0]

    for resource in metadata_dict["result"]["resources"]:
        if "fs_check_info" in resource.keys():
            resource["fs_check_info"] = json.loads(resource["fs_check_info"])
        if "shape_info" in resource.keys():
            resource["shape_info"] = json.loads(resource["shape_info"])

    return metadata_dict


def read_metadata_from_hdx(dataset_name: str) -> dict:
    query_url = f"{CKAN_API_ROOT_URL}package_show"
    params = {"id": dataset_name}
    response = requests.get(query_url, params=params, timeout=20)

    response.raise_for_status()

    metadata_dict = response.json()
    for resource in metadata_dict["result"]["resources"]:
        if "fs_check_info" in resource.keys():
            resource["fs_check_info"] = json.loads(resource["fs_check_info"])
        if "shape_info" in resource.keys():
            resource["shape_info"] = json.loads(resource["shape_info"])
    return metadata_dict


def search_by_lucky_dip() -> dict:
    # log.info('Lucky dip query')
    # Call package search to get a number of datasets (we could hard code this) - filter to
    query_url = f"{CKAN_API_ROOT_URL}package_search"
    count_params = {"fq": "res_format:(CSV and XLS and XLSX)"}
    response = requests.get(query_url, params=count_params, timeout=20)

    response.raise_for_status()
    n_datasets = response.json()["result"]["count"]

    # Now do a 2nd query with a random start, using the first to get the range of possible offsets
    # Make a random offset in the range 0, n datasets
    random_start = randrange(0, n_datasets)
    # query with offset (start) = random, limit (rows) = 1
    random_offset_params = {
        "fq": "res_format:(CSV and XLS and XLSX)",
        "start": random_start,
        "rows": 1,
    }
    response = requests.get(query_url, params=random_offset_params, timeout=20)

    response.raise_for_status()

    metadata_dict = response.json()
    # We do this little trick to make a package_search response for 1 dataset look
    # like a package_show response
    metadata_dict["result"] = metadata_dict["result"]["results"][0]
    for resource in metadata_dict["result"]["resources"]:
        if "fs_check_info" in resource.keys():
            resource["fs_check_info"] = json.loads(resource["fs_check_info"])
        if "shape_info" in resource.keys():
            resource["shape_info"] = json.loads(resource["shape_info"])

    return metadata_dict


def summarise_resource(metadata: dict) -> dict:
    resource_summary = {}
    for resource in metadata["result"]["resources"]:
        resource_summary[resource["name"]] = {}
        resource_summary[resource["name"]]["format"] = resource["format"]
        if "download_url" in resource.keys():
            resource_summary[resource["name"]]["filename"] = resource["download_url"].split("/")[-1]
        else:
            resource_summary[resource["name"]]["filename"] = ""
        resource_summary[resource["name"]]["in_quarantine"] = resource.get("in_quarantine", False)

        resource_summary[resource["name"]]["sheets"] = []

        if "fs_check_info" in resource.keys():
            check, error_message = get_last_complete_check(resource, "fs_check_info")
            if error_message == "Success":
                # print(json.dumps(check, indent=4), flush=True)
                for sheet in check["hxl_proxy_response"]["sheets"]:
                    sheet_name = sheet["name"]
                    nrows = sheet["nrows"]
                    ncols = sheet["ncols"]
                    resource_summary[resource["name"]]["sheets"].append(
                        f"{sheet_name} (n_columns:{ncols} x n_rows:{nrows})"
                    )
        elif "shape_info" in resource.keys():
            check, error_message = get_last_complete_check(resource, "shape_info")
            if error_message == "Success":
                sheet_name = "__DEFAULT__"
                ncols = len(check["layer_fields"])
                nrows = "N/A"
                resource_summary[resource["name"]]["sheets"].append(
                    f"{sheet_name} (n_columns:{ncols} x n_rows:{nrows})"
                )
                resource_summary[resource["name"]]["bounding_box"] = check["bounding_box"]

    if error_message != "Success":
        print(error_message, flush=True)

    return resource_summary


def summarise_resource_changes(metadata: dict) -> dict:
    resource_changes = {}
    for resource in metadata["result"]["resources"]:
        resource_changes[resource["name"]] = {}
        resource_changes[resource["name"]]["checks"] = []

        if "fs_check_info" in resource.keys():
            for check in resource["fs_check_info"]:
                change_indicator = ""
                if check["message"] == "File structure check completed":
                    change_indicator += f"{check['timestamp'][0:10]}"
                    if len(check["sheet_changes"]) != 0:
                        change_indicator += (
                            f"* {len(check['sheet_changes'])} schema changes in field: "
                            f"{check['sheet_changes'][0]['changed_fields'][0]['field']}"
                        )

                    resource_changes[resource["name"]]["checks"].extend([change_indicator])
        elif "shape_info" in resource.keys():
            previous_bounding_box = ""
            previous_headers = set()
            for check in resource["shape_info"]:
                change_indicator = ""
                first_check = True
                if check["message"] == "Import successful":
                    # (json.dumps(check, indent=4), flush=True)
                    headers = {x["field_name"] for x in check["layer_fields"]}
                    bounding_box = check["bounding_box"]
                    change_indicator += f"{check['timestamp'][0:10]}"
                    if not first_check:
                        if (bounding_box != previous_bounding_box) or (previous_headers != headers):
                            change_indicator += "* "
                        if bounding_box != previous_bounding_box:
                            change_indicator += "bounding box change "
                        if previous_headers != headers:
                            change_indicator += "header change"

                    previous_headers = headers
                    previous_bounding_box = bounding_box
                    first_check = False
                    resource_changes[resource["name"]]["checks"].extend([change_indicator])
                # else:
                #     print(json.dumps(check, indent=4), flush=True)

    return resource_changes


def summarise_schema(metadata: dict) -> dict:
    schemas = {}
    for resource in metadata["result"]["resources"]:
        if "fs_check_info" in resource.keys():
            check, error_message = get_last_complete_check(resource, "fs_check_info")

            if error_message == "Success":
                for sheet in check["hxl_proxy_response"]["sheets"]:
                    header_hash = sheet["header_hash"]
                    if header_hash not in schemas:
                        schemas[header_hash] = {}
                        schemas[header_hash]["sheet"] = sheet["name"]
                        schemas[header_hash]["shared_with"] = [resource["name"]]
                        schemas[header_hash]["headers"] = sheet["headers"]
                        schemas[header_hash]["hxl_headers"] = sheet["hxl_headers"]
                        schemas[header_hash]["data_types"] = [""] * len(sheet["headers"])
                    else:
                        schemas[header_hash]["shared_with"].append(resource["name"])
        elif "shape_info" in resource.keys():
            # print(json.dumps(resource["shape_info"][-1], indent=4), flush=True)
            check, error_message = get_last_complete_check(resource, "shape_info")

            # print(json.dumps(check, indent=4), flush=True)
            if error_message == "Success":
                headers = [x["field_name"] for x in check["layer_fields"]]
                data_types = [
                    SHAPE_INFO_DATA_TYPE_LOOKUP[x["data_type"]] for x in check["layer_fields"]
                ]
                header_hash = hash_row(headers)
                if header_hash not in schemas:
                    schemas[header_hash] = {}
                    schemas[header_hash]["sheet"] = "__DEFAULT__"
                    schemas[header_hash]["shared_with"] = [resource["name"]]
                    schemas[header_hash]["headers"] = headers
                    schemas[header_hash]["hxl_headers"] = [""] * len(headers)
                    schemas[header_hash]["data_types"] = data_types
                else:
                    schemas[header_hash]["shared_with"].append(resource["name"])

        if error_message != "Success":
            print(error_message, flush=True)

    return schemas


def get_last_complete_check(resource_metadata: dict, metadata_key: str) -> tuple[dict, str]:
    success = False
    error_message = "Success"
    fingerprint = (
        "Import successful" if metadata_key == "shape_info" else "File structure check completed"
    )
    for check in reversed(resource_metadata[metadata_key]):
        if check["message"] == fingerprint:
            # print(json.dumps(check, indent=4), flush=True)
            success = True
            break
    if not success:
        error_message = (
            f"\nError, could not find an {fingerprint} check "
            f"for {resource_metadata['name']}\n"
            f"final message was '{resource_metadata[metadata_key][-1]['message']}'"
        )
    return check, error_message


def print_schema(schema: dict) -> list[dict]:
    row_template = {"Column": "", "Type": "", "Label": "", "Description": ""}
    rows = []

    if schema["hxl_headers"] is None:
        schema["hxl_headers"] = [""] * len(schema["headers"])

    for i in range(0, len(schema["headers"])):
        row = row_template.copy()
        row["Column"] = schema["headers"][i]
        row["Type"] = schema["data_types"][i]
        row["Label"] = schema["hxl_headers"][i]
        rows.append(row)

    print_table_from_list_of_dicts(rows)
    return rows
