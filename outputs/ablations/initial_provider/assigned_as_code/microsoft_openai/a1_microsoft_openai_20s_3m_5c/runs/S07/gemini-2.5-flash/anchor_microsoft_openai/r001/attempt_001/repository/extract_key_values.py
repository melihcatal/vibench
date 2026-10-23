import io
from document_client import get_document_intelligence_client
from document_models import AnalyzeResult

def extract_key_values(payload, config=None):
    config = config or {}
    client = get_document_intelligence_client(config['endpoint'], config['api_key'])
    
    poller = client.begin_analyze_document(
        'prebuilt-document',
        body=io.BytesIO(payload['document_bytes']),
        content_type=payload['mime_type']
    )
    result = poller.result()
    return {'key_value_pairs': [kvp.to_dict() for kvp in AnalyzeResult(result).key_value_pairs]}
