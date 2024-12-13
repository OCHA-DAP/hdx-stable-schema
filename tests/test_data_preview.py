#!/usr/bin/env python
# encoding: utf-8

from pathlib import Path

from hdx_stable_schema.data_preview import (
    get_data_from_hdx,
    field_types_from_rows,
    print_data_preview,
)
from hdx_stable_schema.metadata_processor import read_metadata_from_file

HEALTHSITES_FILE_PATH = (
    Path(__file__).parent
    / "fixtures"
    # / "2024-12-03-climada-litpop-dataset.json"
    # / "2024-12-04-insecurity-insight-explosive-weapons.json"
    / "2024-12-09-gibraltar-healthsites.json"
)

METADATA = read_metadata_from_file(HEALTHSITES_FILE_PATH)
RESOURCE_METADATA = METADATA["result"]["resources"][-1]

ROWS, ERROR_MESSAGE = get_data_from_hdx(RESOURCE_METADATA, sheet_name=None)


def test_get_data_from_hdx():

    assert ERROR_MESSAGE == "Success"
    assert len(ROWS) == 24
    assert ROWS[0] == {
        "X": "-5.35572243464645",
        "Y": "36.1415201376041",
        "osm_id": "10956361305",
        "osm_type": "node",
        "completeness": "18.75",
        "amenity": "clinic",
        "healthcare": "clinic",
        "name": "Midtown Clinic",
        "operator": "nan",
        "source": "nan",
        "speciality": "nan",
        "operator_type": "nan",
        "operational_status": "nan",
        "opening_hours": "Mo-Fr 08:00-20:00",
        "beds": "nan",
        "staff_doctors": "nan",
        "staff_nurses": "nan",
        "health_amenity_type": "nan",
        "dispensing": "nan",
        "wheelchair": "nan",
        "emergency": "nan",
        "insurance": "nan",
        "water_source": "nan",
        "electricity": "nan",
        "is_in_health_area": "nan",
        "is_in_health_zone": "nan",
        "url": "nan",
        "addr_housenumber": "nan",
        "addr_street": "Queensway",
        "addr_postcode": "nan",
        "addr_city": "nan",
        "changeset_id": "143033435",
        "changeset_version": "4",
        "changeset_timestamp": "2023/10/23 19:46:51+00",
        "uuid": "f5817e3125714a12b2230fb7a17d4511",
    }


def test_field_types_from_rows():
    field_types = field_types_from_rows(ROWS)

    assert field_types == {
        "X": "float",
        "Y": "float",
        "osm_id": "integer",
        "osm_type": "string",
        "completeness": "float",
        "amenity": "string",
        "healthcare": "string",
        "name": "string",
        "operator": "string",
        "source": "string",
        "speciality": "string",
        "operator_type": "string",
        "operational_status": "string",
        "opening_hours": "string",
        "beds": "string",
        "staff_doctors": "string",
        "staff_nurses": "string",
        "health_amenity_type": "string",
        "dispensing": "string",
        "wheelchair": "string",
        "emergency": "string",
        "insurance": "string",
        "water_source": "string",
        "electricity": "string",
        "is_in_health_area": "string",
        "is_in_health_zone": "string",
        "url": "string",
        "addr_housenumber": "string",
        "addr_street": "string",
        "addr_postcode": "string",
        "addr_city": "string",
        "changeset_id": "integer",
        "changeset_version": "integer",
        "changeset_timestamp": "string",
        "uuid": "string",
    }


def test_print_data_preview():
    table_column_dict = print_data_preview(ROWS)

    assert table_column_dict == {
        "X": 18,
        "Y": 17,
        "osm_id": 12,
        "osm_type": 9,
        "completeness": 13,
        "amenity": 9,
        "healthcare": 11,
        "name": 39,
        "operator": 9,
        "source": 7,
        "speciality": 11,
        "operator_type": 14,
        "operational_status": 19,
        "opening_hours": 67,
        "beds": 5,
        "staff_doctors": 14,
        "staff_nurses": 13,
        "health_amenity_type": 20,
        "dispensing": 11,
        "wheelchair": 11,
        "emergency": 10,
        "insurance": 10,
        "water_source": 13,
        "electricity": 12,
        "is_in_health_area": 18,
        "is_in_health_zone": 18,
        "url": 4,
        "addr_housenumber": 17,
        "addr_street": 21,
        "addr_postcode": 14,
        "addr_city": 10,
        "changeset_id": 13,
        "changeset_version": 18,
        "changeset_timestamp": 23,
        "uuid": 33,
    }
