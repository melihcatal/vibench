import os
from .document_client import TableClient
from .document_models import TableResult

def extract_tables(image_path: str) -> TableResult:
    """Extract table cells and row structure using Google Document AI Tables feature.
    """
    client = TableClient()
    response = client.extract_tables(image_path)
    return TableResult(cells=response.get('cells', []), rows=response.get('rows', []))