#!/usr/bin/env python
# encoding: utf-8

from pathlib import Path

from hdx_stable_schema.data_preview import get_data_from_hdx
from hdx_stable_schema.metadata_processor import read_metadata_from_file

HEALTHSITES_FILE_PATH = (
    Path(__file__).parent
    / "fixtures"
    # / "2024-12-03-climada-litpop-dataset.json"
    # / "2024-12-04-insecurity-insight-explosive-weapons.json"
    / "2024-12-09-gibraltar-healthsites.json"
)

METADATA = read_metadata_from_file(HEALTHSITES_FILE_PATH)


def test_get_data_from_hdx():

    resource_metadata = METADATA["result"]["resources"][-1]

    rows, error_message = get_data_from_hdx(resource_metadata, sheet_name=None)

    assert error_message == "Success"
    assert len(rows) == 24
    assert rows[0] == {
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
