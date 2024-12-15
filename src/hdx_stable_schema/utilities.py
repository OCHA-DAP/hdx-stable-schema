#!/usr/bin/env python
# encoding: utf-8

import datetime
import math
import dataclasses
import sys

from pathlib import Path
from typing import Optional

import click
import requests


# This is borrowed from:
# https://github.com/OCHA-DAP/hdx-cli-toolkit/blob/main/src/hdx_cli_toolkit/utilities.py
def print_table_from_list_of_dicts(
    column_data_rows: list[dict[str, str]],
    excluded_fields: None | list[str] = None,
    included_fields: None | list[str] = None,
    truncate_width: int = 130,
    max_total_width: int = 150,
) -> dict:
    """A helper function to print a list of dictionaries as a table

    Arguments:
        column_data_rows {list[dict]} -- the list of dictionaries to print

    Keyword Arguments:
        excluded_fields {None|list} -- any fields to be ommitted, none excluded by default
                                        (default: {None})
        included_fields {None|list} -- any fields to be included, all included by default
                                        (default: {None})
        truncate_width {int} -- width at which to truncate a column (default: {130})
        max_total_width {int} -- total width of the table (default: {150})
    """
    if (len(column_data_rows)) == 0:
        return None
    if dataclasses.is_dataclass(column_data_rows[0]):
        temp_data = []
        for row in column_data_rows:
            temp_data.append(dataclasses.asdict(row))  # type: ignore
        column_data_rows = temp_data

    if excluded_fields is None:
        excluded_fields = []

    if included_fields is None:
        included_fields = list(column_data_rows[0])

    column_table_header_dict = {}
    for field in included_fields:
        widths = [len(str(x[field])) for x in column_data_rows]
        widths.append(len(field))  # .append(len(field))
        max_field_width = max(widths)

        column_table_header_dict[field] = max_field_width + 1
        if max_field_width > truncate_width:
            column_table_header_dict[field] = truncate_width

    # import json

    # print(json.dumps(column_table_header_dict, indent=4), flush=True)
    total_width = (
        sum(v for k, v in column_table_header_dict.items() if k not in excluded_fields)
        + len(column_table_header_dict)
        - 1
    )

    if total_width > max_total_width:
        print(
            f"\nCalculated total_width of {total_width} "
            f"exceeds proposed max_total_width of {max_total_width}. "
            "Showing first row as a dictionary",
            flush=True,
        )
        print_dictionary(column_data_rows[0])
        return column_table_header_dict

    print("-" * total_width, flush=True)

    for k in included_fields:
        if k not in excluded_fields:
            width = column_table_header_dict[k]
            print(f"|{k:<{width}.{width}}", end="", flush=True)
    print("|", flush=True)
    print("-" * total_width, flush=True)

    for row in column_data_rows:
        for k in included_fields:
            value = row[k]

            if k not in excluded_fields:
                width = column_table_header_dict[k]
                print(f"|{str(value):<{width}.{width}}", end="", flush=True)
        print("|", flush=True)

    print("-" * total_width, flush=True)

    return column_table_header_dict


def print_list(list_: list, truncate_width: int = 130, max_total_width: int = 150):
    max_column_width = max([len(x) for x in list_]) + 2
    n_columns = math.floor(max_total_width / (max_column_width))

    for i, element in enumerate(list_, start=1):
        print(f"{element:<{max_column_width}.{max_column_width}}", end="", flush=True)
        if i % n_columns == 0:
            print("", flush=True)
    print("", flush=True)


def print_banner(list_: list[str]):
    timestamp = f"Invoked at: {datetime.datetime.now().isoformat()}"
    lengths = [len(x) for x in list_]
    lengths.append(len(timestamp))
    width = max(lengths)

    click.secho((width + 4) * "*", bold=True)
    for item in list_:
        click.secho(f"* {item:<{width}} *", bold=True)
    click.secho(f"* {timestamp:<{width}} *", bold=True)
    click.secho((width + 4) * "*", bold=True)


def print_dictionary(dictionary: dict):
    max_key_width = max([len(k) for k, _ in dictionary.items()]) + 2
    max_value_width = max([len(v) for _, v in dictionary.items()]) + 2

    total_width = max_key_width + max_value_width
    print("-" * (total_width + 2), flush=True)
    print(
        f"|{'Column':<{max_key_width}.{max_key_width}}|{'Value':<{max_value_width}.{max_value_width}}|",
        flush=True,
    )
    print("-" * (total_width + 2), flush=True)
    for k, v in dictionary.items():
        print(
            f"|{k:<{max_key_width}.{max_key_width}}|{v:<{max_value_width}.{max_value_width}}|",
            flush=True,
        )

    print("-" * (total_width + 2), flush=True)


# Basis borrowed from
# https://stackoverflow.com/a/15645088/19172
def download_from_url(url: str, filename: Optional[str] = None):
    download_directory = Path(__file__).parent / "downloads"
    Path(download_directory).mkdir(parents=True, exist_ok=True)
    if filename is None:
        filename = url.split("/")[-1]

    download_file_path = download_directory / filename

    with open(download_file_path, "wb") as output_file:
        print(f"Downloading {filename}", flush=True)
        response = requests.get(url, stream=True)
        total_length = response.headers.get("content-length")

        if total_length is None:  # no content length header
            output_file.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                output_file.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ("=" * done, " " * (50 - done)))
                sys.stdout.flush()

    return download_file_path
