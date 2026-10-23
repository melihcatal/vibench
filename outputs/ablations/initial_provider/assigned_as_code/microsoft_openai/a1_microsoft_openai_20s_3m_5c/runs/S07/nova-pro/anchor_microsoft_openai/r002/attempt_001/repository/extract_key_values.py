import io
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def extract_key_values(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-keyvalue',
            body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    return {'key_values': result.content}