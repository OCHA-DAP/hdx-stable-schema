#!/usr/bin/env python
# encoding: utf-8

from pathlib import Path

from hdx_stable_schema.metadata_processor import read_metadata_from_file


def test_read_metadata():
    climada_litpop_file_path = (
        Path(__file__).resolve().parents[2]
        / "tests"
        / "fixtures"
        # / "2024-12-03-climada-litpop-dataset.json"
        / "2024-12-04-insecurity-insight-explosive-weapons.json"
    )

    metadata = read_metadata_from_file(climada_litpop_file_path)

    assert metadata is not None
