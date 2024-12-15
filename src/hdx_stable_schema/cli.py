#!/usr/bin/env python
# encoding: utf-8

import sys

import click
import requests

from hdx_stable_schema.metadata_processor import (
    read_metadata_from_hdx,
    search_by_lucky_dip,
    summarise_resource_changes,
    summarise_schema,
    summarise_resource,
    print_schema,
)

from hdx_stable_schema.utilities import print_list, print_banner

from hdx_stable_schema.data_preview import (
    get_data_from_hdx,
    print_data_preview,
    field_types_from_rows,
)


@click.group()
@click.version_option()
def hdx_schema() -> None:
    """Tools for exploring resource schema in HDX"""


# Fetch sample dataset metadata with:
# https://data.humdata.org/api/action/package_show?id=climada-litpop-dataset


@hdx_schema.command(name="show_schema")
@click.option(
    "--dataset_name",
    is_flag=False,
    default=None,
    help="a dataset name or pattern on which to filter list",
)
def show_schema(dataset_name: str):
    """Show a resource view with a Data Dictionary and a data preview"""

    # Get some metadata some how
    if dataset_name is not None:
        try:
            metadata = read_metadata_from_hdx(dataset_name)
        except requests.exceptions.HTTPError as exception_:
            if exception_.args[0].startswith("404"):
                print(f"Dataset '{dataset_name}' was not found", flush=True)
                sys.exit()
            else:
                raise
    else:
        metadata = search_by_lucky_dip()

    # Derive summaries

    resource_summary = summarise_resource(metadata)
    resource_changes = summarise_resource_changes(metadata)
    schemas = summarise_schema(metadata)

    # Do things with Data Previews?
    # 1. Derive data types
    # 2. Show a data preview table

    # Print dataset page

    # Print Dataset intro
    print_banner([metadata["result"]["title"], "Dataset Overview"])
    # Rerun command
    print(
        "Rerun command: \nhdx-schema show_dataset "
        f"--dataset_name='{metadata['result']['name']}'\n"
    )
    # Print Resource list
    print("Resource list:", flush=True)
    print_resource_summary(resource_summary, resource_changes)

    # Print schemas
    if len(schemas) == 1:
        print("\nFound one common schema", flush=True)
    else:
        print(f"\nFound {len(schemas)} common schemas")

    for i, schema in enumerate(schemas.items(), start=1):
        print(
            f"\nSchema {i}, shared by the following {len(schema[1]['shared_with'])} "
            f"resources on sheet '{schema[1]['sheet']}':\n",
            flush=True,
        )
        print_list(schema[1]["shared_with"])

        print("\nData Dictionary", flush=True)
        print_schema(schema[1])


@hdx_schema.command(name="preview_resource")
@click.option(
    "--dataset_name",
    is_flag=False,
    default=None,
    help="a dataset name",
)
@click.option(
    "--resource_name",
    is_flag=False,
    default=None,
    help="a resource name",
)
def preview_resource(dataset_name: str, resource_name: str):
    """Show a dataset with schema markup"""

    # Get some metadata some how
    if dataset_name is not None:
        try:
            metadata = read_metadata_from_hdx(dataset_name)
        except requests.exceptions.HTTPError as exception_:
            if exception_.args[0].startswith("404"):
                print(f"Dataset '{dataset_name}' was not found", flush=True)
                sys.exit()
            else:
                raise
    else:
        metadata = search_by_lucky_dip()
        resource_name = None

    if resource_name is None:
        for resource in metadata["result"]["resources"]:
            print(resource["name"], resource["format"], flush=True)
            if resource["format"].lower() in ["csv", "xlsx", "csv", "geojson"]:
                resource_name = resource["name"]
                break

    # Print Resource Overview
    dataset_name = metadata["result"]["name"]
    print_banner(
        [f"Dataset name: {dataset_name}", f"Resource name: {resource_name}", "Resource Overview"]
    )

    # Rerun command
    print(
        "Rerun command: \nhdx-schema preview_resource "
        f"--dataset_name='{dataset_name}' "
        f"--resource_name='{resource_name}'"
    )
    # Derive summaries
    print("\nCollecting metadata...", flush=True)
    resource_summary = summarise_resource(metadata)
    resource_changes = summarise_resource_changes(metadata)
    schemas = summarise_schema(metadata)

    resource_metadata = None
    for resource in metadata["result"]["resources"]:
        if resource["name"] == resource_name:
            resource_metadata = resource
            break

    assert resource_metadata is not None, (
        f"Resource '{resource_name}' not " f"found in dataset '{dataset_name}'"
    )

    print("\nDownloading data preview...", flush=True)
    preview_data, error_message = get_data_from_hdx(resource_metadata, None)
    if error_message != "Success":
        print(error_message, flush=True)
        sys.exit()

    # Decorate Data Dictionary with data types
    add_data_types = False
    if resource_metadata["format"].lower() in ["csv", "xlsx", "xls"]:
        field_types = field_types_from_rows(preview_data)
        add_data_types = True

    for _, schema in schemas.items():
        if resource_name in schema["shared_with"]:
            if add_data_types:
                schema["data_types"] = [v for k, v in field_types.items()]
            break

    print("\nResource summary:", flush=True)
    print_resource_summary(resource_summary, resource_changes, target_resource_name=resource_name)

    # Print Data Dictionary
    print(
        f"\nSchema for {resource_name} shared with the following {len(schema['shared_with'])} "
        f"resources on sheet '{schema['sheet']}':\n",
        flush=True,
    )
    print_list(schema["shared_with"])
    print("\nData Dictionary", flush=True)
    print_schema(schema)
    # Print data preview
    print("\nData Preview (first 10 lines)", flush=True)
    print_data_preview(preview_data[0:10])


def print_resource_summary(resource_summary, resource_changes, target_resource_name=None):
    if target_resource_name is None:
        resource_names = list(resource_changes.keys())
    else:
        resource_names = [target_resource_name]
    for i, resource_name in enumerate(resource_names, start=1):
        checks = resource_changes[resource_name]["checks"]
        print(f"\n{i:>2d}. {resource_name}", flush=True)
        print(
            f"\tFilename: {resource_summary[resource_name]['filename']} "
            f"\n\tFormat: {resource_summary[resource_name]['format']}"
            f"\n\tSheets: {', '.join(resource_summary[resource_name]['sheets'])}",
            flush=True,
        )
        if "bounding_box" in resource_summary[resource_name].keys():
            print(f"\tBounding box: {resource_summary[resource_name]['bounding_box']}", flush=True)
        if resource_summary[resource_name]["in_quarantine"]:
            print("\t**in quarantine**", flush=True)
        print(f"\tChecks ({len(checks)} file structure checks):", flush=True)
        for check in checks:
            print(f"\t\t{check}", flush=True)
