#!/usr/bin/env python
# encoding: utf-8

import json

from pathlib import Path

from hdx_stable_schema.metadata_processor import (
    read_metadata_from_file,
    summarise_schema,
    summarise_resource,
)

HEALTHSITES_FILE_PATH = (
    Path(__file__).parent
    / "fixtures"
    # / "2024-12-03-climada-litpop-dataset.json"
    # / "2024-12-04-insecurity-insight-explosive-weapons.json"
    / "2024-12-09-gibraltar-healthsites.json"
)

METADATA = read_metadata_from_file(HEALTHSITES_FILE_PATH)


def test_read_metadata():
    assert METADATA is not None


def test_table_schema():
    schemas_file_path = (
        Path(__file__).parent / "fixtures" / "2024-12-09-gibraltar-healthsites-schemas.json"
    )

    schemas = summarise_schema(METADATA)
    with open(schemas_file_path, encoding="utf-8") as schemas_file:
        expected_schemas = json.load(schemas_file)

    assert schemas == expected_schemas


def test_summarise_resources():
    resource_summary_file_path = (
        Path(__file__).parent / "fixtures" / "2024-12-09-gibraltar-healthsites-resource.json"
    )

    resource_summary = summarise_resource(METADATA)

    with open(resource_summary_file_path, encoding="utf-8") as resource_file:
        expected_resource_summary = json.load(resource_file)

    assert expected_resource_summary == resource_summary
