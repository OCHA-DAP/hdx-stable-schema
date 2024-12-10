#!/usr/bin/env python
# encoding: utf-8

from hdx_stable_schema.utilities import print_banner, print_table_from_list_of_dicts, print_list


def test_print_banner(capfd):
    print_banner(["test_action"])
    output, errors = capfd.readouterr()

    assert errors == ""
    parts = output.split("\n")
    assert len(parts) == 5
    for part in parts:
        if len(part) == 0:
            continue
        assert len(part) == 42


def test_print_table_from_list_of_dicts(capfd):
    test_data = [{"column a": "a", "column b": "b", "column c": "c"}]
    print_table_from_list_of_dicts(test_data)

    output, errors = capfd.readouterr()
    assert errors == ""
    parts = output.split("\n")
    assert len(parts) == 6
    for part in parts:
        if len(part) == 0:
            continue
        assert len(part) in [29, 31]


def test_print_list(capfd):
    test_data = ["long test name"] * 20
    print_list(test_data)

    output, errors = capfd.readouterr()

    assert errors == ""
    parts = output.split("\n")
    assert len(parts) == 4
    for part in parts:
        assert len(part) in [144, 32, 0]
