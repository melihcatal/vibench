from typing import List
from document_client import DocumentClient
from document_models import normalize_tables, Table


def extract_tables(image_bytes: bytes) -> List[Table]:
    client = DocumentClient()
    response = client.process_document(image_bytes)
    return normalize_tables(response)
