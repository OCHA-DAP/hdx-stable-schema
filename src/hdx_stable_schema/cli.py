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

    # Dataset intro
    print_banner([metadata["result"]["title"], "Dataset Overview"])
    print(f"Dataset name: {metadata['result']['name']}", flush=True)

    # Summarise and print resource changes
    print("Resource list:", flush=True)
    resource_summary = summarise_resource(metadata)
    resource_changes = summarise_resource_changes(metadata)
    for i, resource_name in enumerate(resource_changes.keys(), start=1):
        checks = resource_changes[resource_name]["checks"]
        print(f"\n{i:>2d}. {resource_name}", flush=True)
        print(
            f"\tFilename: {resource_summary[resource_name]['filename']} "
            f"\n\tFormat: {resource_summary[resource_name]['format']}"
            f"\n\tSheets: {', '.join(resource_summary[resource_name]['sheets'])}",
            flush=True,
        )
        if resource_summary[resource_name]["in_quarantine"]:
            print("\t**in quarantine**", flush=True)
        print(f"\tChecks ({len(checks)} file structure checks):", flush=True)
        for check in checks:
            print(f"\t\t{check}", flush=True)

    # Summarise and print schemas
    schemas = summarise_schema(metadata)

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
