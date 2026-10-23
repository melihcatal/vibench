import io
from document_client import make_client


def extract_key_values(payload, config=None):
    with make_client(config) as client:
        result = client.begin_analyze_document('prebuilt-document', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    return {'key_values': [{'key': getattr(kv.key, 'content', None), 'value': getattr(kv.value, 'content', None)} for kv in getattr(result, 'key_value_pairs', []) or []]}
