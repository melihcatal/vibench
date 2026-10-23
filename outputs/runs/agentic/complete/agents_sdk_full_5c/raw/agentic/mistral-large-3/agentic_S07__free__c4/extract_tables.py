import os
from typing import Dict, Any, List
import requests
from document_client import get_document_client
from document_models import TableExtractionResponse, TableCell


def extract_tables(image_path: str) -> TableExtractionResponse:
    """
    Extract tables and their cell structures from a document using Microsoft Azure Form Recognizer.
    """
    client = get_document_client("form_recognizer")
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    # Microsoft Azure Form Recognizer-specific request
    response = client.post(
        f"https://{os.getenv('AZURE_FORM_RECOGNIZER_ENDPOINT')}/formrecognizer/documentModels/prebuilt-layout:analyze?api-version=2023-07-31",
        headers={"Content-Type": "application/octet-stream"},
        data=content
    )
    
    response.raise_for_status()
    operation_url = response.headers["Operation-Location"]
    
    # Poll for results
    result = None
    while True:
        status_response = client.get(operation_url)
        status_response.raise_for_status()
        status_result = status_response.json()
        if status_result["status"] in ["succeeded", "failed"]:
            result = status_result
            break
    
    if result["status"] != "succeeded":
        raise ValueError("Table extraction failed")
    
    # Normalize response to local model
    tables = []
    for table in result["analyzeResult"]["tables"]:
        cells = []
        for cell in table["cells"]:
            cells.append(
                TableCell(
                    row_index=cell["rowIndex"],
                    column_index=cell["columnIndex"],
                    text=cell.get("content", ""),
                    bounding_box={
                        "left": cell["boundingRegions"][0]["polygon"][0]["x"],
                        "top": cell["boundingRegions"][0]["polygon"][0]["y"],
                        "width": cell["boundingRegions"][0]["polygon"][2]["x"] - cell["boundingRegions"][0]["polygon"][0]["x"],
                        "height": cell["boundingRegions"][0]["polygon"][2]["y"] - cell["boundingRegions"][0]["polygon"][0]["y"]
                    }
                )
            )
        tables.append({"cells": cells})
    
    return TableExtractionResponse(tables=tables, provider="microsoft_azure_form_recognizer")