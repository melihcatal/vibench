from typing import Dict, List, Optional
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_client import (
    get_azure_form_recognizer_client,
    get_azure_form_recognizer_endpoint,
)
from document_models import TableResponse


def extract_tables(image_path: str) -> TableResponse:
    """Extract tables from a document using Azure Form Recognizer."""
    endpoint = get_azure_form_recognizer_endpoint()
    credential = AzureKeyCredential(os.getenv("AZURE_FORM_RECOGNIZER_KEY"))
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
                        "bounding_box": [
                            {"x": point.x, "y": point.y}
                            for point in cell.bounding_regions[0].polygon
                        ]
                        if cell.bounding_regions
                        else [],
                    }
                )
            rows.append({"cells": cells})

        tables.append(
            {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "rows": rows,
                "bounding_box": [
                    {"x": point.x, "y": point.y}
                    for point in table.bounding_regions[0].polygon
                ]
                if table.bounding_regions
                else [],
            }
        )

    return TableResponse(tables=tables)
