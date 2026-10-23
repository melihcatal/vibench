import io
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def extract_tables(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-read',
            body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    return {'tables': result.tables}