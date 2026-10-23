from document_client import DocumentClient
from document_models import normalize_text, PlainText


def extract_text(image_bytes: bytes) -> str:
    client = DocumentClient()
    response = client.process_document(image_bytes)
    normalized: PlainText = normalize_text(response)
    return normalized["text"]
