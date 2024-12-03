#!/usr/bin/env python
# encoding: utf-8

import json

from pathlib import Path

from hdx_stable_schema.utilities import print_table_from_list_of_dicts


def read_metadata(file_path: str | Path) -> dict:
    metadata_dict = {}

    with open(file_path, encoding="utf-8") as metadata_file:
        metadata_dict = json.load(metadata_file)

    for resource in metadata_dict["result"]["resources"]:
        if "fs_check_info" in resource.keys():
            resource["fs_check_info"] = json.loads(resource["fs_check_info"])

    return metadata_dict


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
                            f"* {len(check['sheet_changes'])} "
                            f"{check['sheet_changes'][0]['changed_fields'][0]['field']}"
                        )
                    resource_changes[resource["name"]]["checks"].extend([change_indicator])

    return resource_changes


def summarise_schema(metadata: dict) -> dict:
    schemas = {}
    for resource in metadata["result"]["resources"]:
        if "fs_check_info" in resource.keys():
            check = resource["fs_check_info"][-1]
            if check["message"] == "File structure check completed":
                header_hash = check["hxl_proxy_response"]["sheets"][0]["header_hash"]
                if header_hash not in schemas:
                    schemas[header_hash] = {}
                    schemas[header_hash]["shared_with"] = [resource["name"]]
                    schemas[header_hash]["headers"] = check["hxl_proxy_response"]["sheets"][0][
                        "headers"
                    ]
                    schemas[header_hash]["hxl_headers"] = check["hxl_proxy_response"]["sheets"][0][
                        "hxl_headers"
                    ]
                else:
                    schemas[header_hash]["shared_with"].append(resource["name"])
            else:
                print(
                    "Error, final fs_check_info is not 'File structure check completed'", flush=True
                )

    return schemas


def print_schema(schema: dict) -> list[dict]:
    row_template = {"Column": "", "Type": "", "Label": "", "Description": ""}
    rows = []
    for header, hxl_header in zip(schema["headers"], schema["hxl_headers"]):
        row = row_template.copy()
        row["Column"] = header
        row["Label"] = hxl_header
        rows.append(row)

    print_table_from_list_of_dicts(rows)
    return rows
