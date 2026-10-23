import io

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_models import normalize_payload


def extract_layout(payload, config=None):
    payload = normalize_payload(payload)
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-layout', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    return {'pages': [page.to_dict() if hasattr(page, 'to_dict') else page for page in getattr(result, 'pages', [])], 'tables': [table.to_dict() if hasattr(table, 'to_dict') else table for table in getattr(result, 'tables', [])], 'content': getattr(result, 'content', '')}
