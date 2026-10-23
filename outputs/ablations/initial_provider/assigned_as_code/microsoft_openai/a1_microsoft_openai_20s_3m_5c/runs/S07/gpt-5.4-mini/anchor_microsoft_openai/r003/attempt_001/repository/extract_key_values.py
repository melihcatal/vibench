from document_client import get_client, analyze_document
from document_models import normalize_key_values


def extract_key_values(payload, config=None):
    with get_client(config) as client:
        result = analyze_document(client, 'prebuilt-document', payload['document_bytes'], payload['mime_type'])
    return {'key_value_pairs': normalize_key_values(result)}
