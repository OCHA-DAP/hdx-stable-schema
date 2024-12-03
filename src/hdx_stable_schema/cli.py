#!/usr/bin/env python
# encoding: utf-8

import click

from pathlib import Path

from hdx_stable_schema.metadata_processor import (
    read_metadata,
    summarise_resource_changes,
    summarise_schema,
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
def show_schema():
    """Show a dataset with schema markup"""

    climada_litpop_file_path = (
        Path(__file__).resolve().parents[2]
        / "tests"
        / "fixtures"
        / "2024-12-03-climada-litpop-dataset.json"
    )

    metadata = read_metadata(climada_litpop_file_path)

    # Dataset intro
    print_banner([metadata["result"]["title"], "Dataset Overview"])

    # Summarise and print resource changes
    print("Resource list:", flush=True)
    resource_changes = summarise_resource_changes(metadata)
    for i, resource_name in enumerate(resource_changes.keys(), start=1):
        checks = resource_changes[resource_name]["checks"]
        print(f"{i:>2d}. {resource_name} ({len(checks)} file structure checks)", flush=True)
        for check in checks:
            print(f"\t{check}", flush=True)

    # Summarise and print schemas
    schemas = summarise_schema(metadata)
    if len(schemas) == 1:
        print("\nFound one common schema", flush=True)
    else:
        print(f"\nFound {len(schemas)} common schemas")
    for i, schema in enumerate(schemas.items(), start=1):
        print(
            f"\nSchema {i}, shared by the following {len(schema[1]['shared_with'])} resources:\n",
            flush=True,
        )
        print_list(schema[1]["shared_with"])

        print("\nData Dictionary", flush=True)
        print_schema(schema[1])
