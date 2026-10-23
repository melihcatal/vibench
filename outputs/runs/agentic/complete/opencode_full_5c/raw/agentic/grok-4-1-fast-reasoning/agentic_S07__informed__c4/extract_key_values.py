from typing import List
from document_client import DocumentClient
from document_models import normalize_key_values, KeyValue


def extract_key_values(image_bytes: bytes) -> List[KeyValue]:
    client = DocumentClient()
    response = client.process_document(image_bytes)
    return normalize_key_values(response)
