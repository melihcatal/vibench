import io

from document_client import create_document_client, load_document_config
from document_models import extract_key_values as normalize_key_values, normalize_payload


def extract_key_values(payload, config=None):
    payload = normalize_payload(payload)
    config = load_document_config(config)
    with create_document_client(config) as client:
        result = client.begin_analyze_document('prebuilt-document', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    return {'key_values': normalize_key_values(result)}
