import os
from typing import List, Dict, Any
import requests
from document_client import get_azure_form_recognizer_client
from document_models import (
    TableExtractionRequest,
    TableExtractionResponse,
    Table,
    TableCell,
)


def extract_tables(image_path: str) -> TableExtractionResponse:
    """
    Extract table cells and row structure from a document using Azure Form Recognizer.
    """
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    api_key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Form Recognizer credentials not configured")

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/octet-stream",
    }

    url = f"{endpoint}/formrecognizer/documentModels/prebuilt-layout:analyze?api-version=2023-07-31"

    response = requests.post(url, headers=headers, data=image_data)
    response.raise_for_status()

    operation_location = response.headers["Operation-Location"]

    result_response = requests.get(
        operation_location, headers={"Ocp-Apim-Subscription-Key": api_key}
    )
    result_response.raise_for_status()
    result = result_response.json()

    tables = []
    for table_data in result.get("analyzeResult", {}).get("tables", []):
        cells = []
        for cell_data in table_data.get("cells", []):
            cell = TableCell(
                row_index=cell_data.get("rowIndex", 0),
                column_index=cell_data.get("columnIndex", 0),
                content=cell_data.get("content", ""),
                bounding_regions=cell_data.get("boundingRegions", []),
            )
            cells.append(cell)

        table = Table(
            row_count=table_data.get("rowCount", 0),
            column_count=table_data.get("columnCount", 0),
            cells=cells,
            bounding_regions=table_data.get("boundingRegions", []),
        )
        tables.append(table)

    return TableExtractionResponse(
        tables=tables, provider="azure_form_recognizer", raw_response=result
    )
