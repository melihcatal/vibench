import io
from document_client import get_document_intelligence_client
from document_models import AnalyzeResult

def extract_tables(payload, config=None):
    config = config or {}
    client = get_document_intelligence_client(config['endpoint'], config['api_key'])
    
    poller = client.begin_analyze_document(
        'prebuilt-layout',
        body=io.BytesIO(payload['document_bytes']),
        content_type=payload['mime_type']
    )
    result = poller.result()
    return {'tables': [table.to_dict() for table in AnalyzeResult(result).tables]}
