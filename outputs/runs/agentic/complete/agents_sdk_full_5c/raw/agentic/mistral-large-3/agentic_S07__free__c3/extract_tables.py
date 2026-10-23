from typing import List, Dict, Any
import requests
import os
from document_client import get_document_client
from document_models import TableExtractionResponse, Table, TableCell


def extract_tables(image_path: str) -> TableExtractionResponse:
    """
    Extract tables from a document using Microsoft Azure Form Recognizer.
    """
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    api_key = os.getenv("AZURE_FORM_RECOGNIZER_API_KEY")
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    # Azure Form Recognizer API-specific request for table extraction
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": api_key
    }
    
    response = requests.post(
        f"{endpoint}/formrecognizer/documentModels/prebuilt-layout:analyze?readingOrder=natural",
        headers=headers,
        data=content
    )
    response.raise_for_status()
    
    operation_url = response.headers["Operation-Location"]
    result = _poll_azure_operation(operation_url, api_key)
    
    tables = []
    if "tables" in result:
        for table in result["tables"]:
            cells = []
            for cell in table.get("cells", []):
                cells.append(
                    TableCell(
                        row_index=cell.get("rowIndex", 0),
                        column_index=cell.get("columnIndex", 0),
                        text=cell.get("content", ""),
                        bounding_box=cell.get("boundingRegions", [{}])[0].get("polygon", []),
                        confidence=cell.get("confidence", 0.0)
                    )
                )
            tables.append(
                Table(
                    row_count=table.get("rowCount", 0),
                    column_count=table.get("columnCount", 0),
                    cells=cells
                )
            )
    
    return TableExtractionResponse(
        tables=tables,
        provider="azure_form_recognizer",
        raw_response=result
    )


def _poll_azure_operation(operation_url: str, api_key: str) -> Dict[str, Any]:
    """Poll Azure Form Recognizer operation until completion."""
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    while True:
        response = requests.get(operation_url, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result.get("status") in ["succeeded", "failed"]:
            return result.get("analyzeResult", {}) if result.get("status") == "succeeded" else {}
        time.sleep(2)