from __future__ import annotations

from document_client import DEFAULT_LAYOUT_MODEL, create_document_client, read_bytes
from document_models import as_dict_list, normalize_table_cells


def extract_tables(file_path: str) -> dict:
    client = create_document_client()
    poller = client.begin_analyze_document(
        DEFAULT_LAYOUT_MODEL, body=read_bytes(file_path)
    )
    result = poller.result()
    cells = normalize_table_cells(result)
    tables = []
    for table in getattr(result, "tables", []) or []:
        tables.append(
            {
                "row_count": getattr(table, "row_count", None),
                "column_count": getattr(table, "column_count", None),
                "page": (
                    table.bounding_regions[0].page_number
                    if getattr(table, "bounding_regions", None)
                    else 1
                ),
            }
        )
    return {
        "provider": "azure-document-intelligence",
        "model_id": DEFAULT_LAYOUT_MODEL,
        "tables": tables,
        "cells": as_dict_list(cells),
    }
