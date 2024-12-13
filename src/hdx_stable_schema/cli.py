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
    """Tools for exploring schema in HDX"""


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
    print(f"Dataset name: {metadata['result']['name']}", flush=True)

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

    # Derive summaries

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

    preview_data, error_message = get_data_from_hdx(resource_metadata, None)

    assert error_message == "Success", "Failed to load preview data"
    # Decorate Data Dictionary with data types
    field_types = field_types_from_rows(preview_data)
    for _, schema in schemas.items():
        if resource_name in schema["shared_with"]:
            schema["data_types"] = [v for k, v in field_types.items()]
            break

    # Print Resource Overview
    print_banner(
        [f"Dataset name: {dataset_name}", f"Resource name: {resource_name}", "Resource Overview"]
    )

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
