import io

from document_client import create_document_client, load_document_config
from document_models import extract_tables as normalize_tables, normalize_payload


def extract_tables(payload, config=None):
    payload = normalize_payload(payload)
    config = load_document_config(config)
    with create_document_client(config) as client:
        result = client.begin_analyze_document('prebuilt-layout', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    return {'tables': normalize_tables(result)}
