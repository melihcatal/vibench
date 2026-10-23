from typing import List, Dict, Optional
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_azure_form_recognizer_client
from document_models import TableResponse, Table


def extract_tables(image_path: str) -> TableResponse:
    """Extract tables from a document using Azure Form Recognizer."""
    client = get_azure_form_recognizer_client()

    with open(image_path, "rb") as image_file:
        poller = client.begin_analyze_document("prebuilt-layout", image_file)

    result = poller.result()
    tables = []

    for table in result.tables:
        rows = []
        for row in table.rows:
            cells = []
            for cell in row.cells:
                cells.append(
                    {
                        "text": cell.content,
                        "row_index": cell.row_index,
                        "column_index": cell.column_index,
                        "bounding_box": {
                            "vertices": [
                                {"x": point.x, "y": point.y}
                                for point in cell.bounding_regions[0].polygon
                            ]
                            if cell.bounding_regions
                            else []
                        },
                    }
                )
            rows.append({"cells": cells})

        tables.append(
            Table(
                rows=rows,
                bounding_box={
                    "vertices": [
                        {"x": point.x, "y": point.y}
                        for point in table.bounding_regions[0].polygon
                    ]
                    if table.bounding_regions
                    else []
                },
            )
        )

    return TableResponse(provider="azure_form_recognizer", tables=tables)
