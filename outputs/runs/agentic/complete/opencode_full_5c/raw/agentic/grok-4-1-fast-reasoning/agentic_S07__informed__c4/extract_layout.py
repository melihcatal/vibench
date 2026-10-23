from typing import List
from document_client import DocumentClient
from document_models import normalize_layout, LayoutBlock


def extract_layout(image_bytes: bytes) -> List[LayoutBlock]:
    client = DocumentClient()
    response = client.process_document(image_bytes)
    return normalize_layout(response)
