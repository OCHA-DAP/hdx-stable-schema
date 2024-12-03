#!/usr/bin/env python
# encoding: utf-8

import click


@click.group()
@click.version_option()
def hdx_schema() -> None:
    """Tools for exploring schema in HDX"""
