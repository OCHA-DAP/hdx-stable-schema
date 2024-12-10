#!/usr/bin/env python
# encoding: utf-8

import pandas

from typing import Optional


def get_data_from_hdx(resource_metadata: dict, sheet_name: Optional[str]) -> tuple[list[dict], str]:
    download_url = resource_metadata["download_url"]
    file_format = resource_metadata["format"]
    results = []
    error_message = "Success"
    try:
        if file_format.upper() in ["XLS", "XLSX"]:
            if sheet_name is None:
                dataframe = pandas.read_excel(download_url)
            else:
                dataframe = pandas.read_excel(download_url, sheet_name=sheet_name)
        elif file_format == "CSV":
            dataframe = pandas.read_csv(download_url)
        else:
            error_message = f"Data in file format {file_format} not supported"
        dataframe = dataframe.astype(str)
        results = dataframe.to_dict("records")

    except FileNotFoundError:
        error_message = f"Resource not found for URL {download_url}"
    except pandas.errors.ParserError:
        error_message = f"Resource could not be parsed for URL {download_url}"
    except UnicodeDecodeError:
        error_message = f"Unicode error for URL {download_url}"

    return results, error_message
