import io

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def extract_key_values(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-document', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    pairs = []
    for kv in getattr(result, 'key_value_pairs', []) or []:
        key = getattr(kv.key, 'content', None) if kv.key else None
        value = getattr(kv.value, 'content', None) if kv.value else None
        pairs.append({'key': key, 'value': value, 'confidence': getattr(kv, 'confidence', None)})
    return {'key_values': pairs}
