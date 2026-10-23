from document_client import get_client, analyze_document
from document_models import normalize_layout


def extract_layout(payload, config=None):
    with get_client(config) as client:
        result = analyze_document(client, 'prebuilt-layout', payload['document_bytes'], payload['mime_type'])
    return normalize_layout(result)
