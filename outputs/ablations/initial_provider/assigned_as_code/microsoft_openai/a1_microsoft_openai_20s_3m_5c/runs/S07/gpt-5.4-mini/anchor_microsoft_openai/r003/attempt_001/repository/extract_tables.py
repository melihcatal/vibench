from document_client import get_client, analyze_document
from document_models import normalize_tables


def extract_tables(payload, config=None):
    with get_client(config) as client:
        result = analyze_document(client, 'prebuilt-layout', payload['document_bytes'], payload['mime_type'])
    return {'tables': normalize_tables(result)}
