import io

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_models import normalize_payload


def extract_key_values(payload, config=None):
    payload = normalize_payload(payload)
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-document', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    pairs = []
    for item in getattr(result, 'key_value_pairs', []):
        key = getattr(item, 'key', None)
        value = getattr(item, 'value', None)
        pairs.append({'key': getattr(key, 'content', None) if key else None, 'value': getattr(value, 'content', None) if value else None})
    return {'key_values': pairs}
