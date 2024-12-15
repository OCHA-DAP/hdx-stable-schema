#!/usr/bin/env python
# encoding: utf-8

import ast
import datetime
import glob
import shutil
import sys
import zipfile

import pandas
import geopandas

from pathlib import Path


from collections import Counter
from typing import Optional
from hdx_stable_schema.utilities import print_table_from_list_of_dicts, download_from_url
from hdx_stable_schema.metadata_processor import get_last_complete_check


def get_data_from_hdx(resource_metadata: dict, sheet_name: Optional[str]) -> tuple[list[dict], str]:
    download_url = resource_metadata["download_url"]
    file_format = resource_metadata["format"]
    results = []
    error_message = "Success"
    metadata_key = "fs_check_info"
    try:
        if file_format.upper() in ["XLS", "XLSX"]:
            if sheet_name is None:
                dataframe = pandas.read_excel(download_url)
            else:
                dataframe = pandas.read_excel(download_url, sheet_name=sheet_name)
        elif file_format == "CSV":
            dataframe = pandas.read_csv(download_url)
        elif file_format in ["GeoJSON", "SHP"]:
            metadata_key = "shape_info"
            local_file_path, error_message = download_from_url(download_url)
            if error_message == "Success":
                dataframe, error_message = load_dataframe_from_local_path(
                    str(local_file_path), file_format
                )
            shutil.rmtree(Path(local_file_path).parent)
        else:
            error_message = f"Data in file format {file_format} not supported"
        dataframe = dataframe.astype(str)
        results = dataframe.to_dict("records")
        is_hxlated = False
        check, error_message = get_last_complete_check(resource_metadata, metadata_key)
        if "hxl_proxy_response" in check:
            if len(check["hxl_proxy_response"]["sheets"]) == 1:
                is_hxlated = check["hxl_proxy_response"]["sheets"][0]["is_hxlated"]
            else:
                print("More than 1 sheet, not implemented scanning for the right sheet", flush=True)
                sys.exit()

        if is_hxlated:
            results = results[1:]

    except FileNotFoundError:
        error_message = (
            f"Resource not found for URL {download_url}"
            if error_message == "Success"
            else error_message
        )
    except pandas.errors.ParserError:
        error_message = (
            f"Resource could not be parsed for URL {download_url}"
            if error_message == "Success"
            else error_message
        )
    except UnicodeDecodeError:
        error_message = (
            f"Unicode error for URL {download_url}" if error_message == "Success" else error_message
        )
    except (UnboundLocalError, ValueError):
        error_message = (
            (
                f"Unknown failure for resource_name '{resource_metadata['name']}' "
                f"with download_url {resource_metadata['download_url']}"
            )
            if error_message == "Success"
            else error_message
        )

    return results, error_message


def print_data_preview(rows: list[dict]) -> dict:
    return print_table_from_list_of_dicts(rows)


def field_types_from_rows(rows: list[dict], null_equivalents: Optional[list] = None) -> dict:
    if null_equivalents is None:
        null_equivalents = ["", None]
    field_types = {}
    for column_name in rows[0].keys():
        column = [x[column_name] for x in rows]
        field_type = field_type_from_column(column, null_equivalents=null_equivalents)
        field_types[column_name] = field_type

    return field_types


def field_type_from_column(
    column: list, null_equivalents: Optional[list] = None, strict: bool = False
) -> str:
    if null_equivalents is None:
        null_equivalents = ["", None]
    python_type_to_type = {
        "str": "string",
        "int": "integer",
        "float": "float",
        "bool": "bool",
        "list": "list",
        "DATE": "date",
        "DATETIME": "datetime",
    }

    field_type = "TEXT"
    type_counter = Counter()
    for string in column:
        if string in null_equivalents:
            continue
        try:
            value = ast.literal_eval(f"{string}")
            type_ = type(value).__name__
        except (ValueError, SyntaxError):
            type_ = "str"

        if type_ == "str":
            try:
                datetime.datetime.strptime(string, "%Y-%m-%d")
                type_ = "DATE"
            except (ValueError, TypeError):
                pass
        if type_ == "str":
            try:
                datetime.datetime.fromisoformat(string)
                type_ = "DATETIME"
            except (ValueError, TypeError):
                pass
        if isinstance(string, datetime.datetime):
            type_ = "DATETIME"
        type_counter[type_] += 1

    if set(type_counter.keys()) == set(["float", "int"]):
        field_type = "float"
    elif strict and len(type_counter) != 1:
        field_type = "string"
    else:
        field_type = python_type_to_type[type_counter.most_common(1)[0][0]]

    return field_type


def load_dataframe_from_local_path(
    local_file_path: str, file_format: str
) -> tuple[geopandas.GeoDataFrame, str]:
    error_message = "Success"
    if str(local_file_path).lower().endswith(".zip"):
        unzip_directory = Path(local_file_path).parent
        with zipfile.ZipFile(local_file_path, "r") as zip_file:
            zip_file.extractall(unzip_directory)
        glob_path = str(Path(unzip_directory) / "**" / f"*.{file_format.lower()}")
        print(f"glob_path: {glob_path}", flush=True)
        geo_files = sorted(glob.glob(glob_path))
        error_message = "Got more than one file of the right format from a zip"
        local_file_path = str(geo_files[0])

    dataframe = geopandas.read_file(local_file_path)

    return dataframe, error_message
