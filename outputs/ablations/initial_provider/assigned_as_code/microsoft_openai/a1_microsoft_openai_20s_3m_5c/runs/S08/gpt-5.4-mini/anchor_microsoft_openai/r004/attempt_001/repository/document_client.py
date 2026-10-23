import io
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def load_document_config(config=None):
    data = dict(config or {})
    if 'endpoint' not in data:
        data['endpoint'] = os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
    if 'api_key' not in data:
        data['api_key'] = os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_API_KEY')
    return data


def create_document_client(config=None):
    data = load_document_config(config)
    return DocumentIntelligenceClient(data['endpoint'], AzureKeyCredential(data['api_key']))


def analyze_document(model_id, payload, config=None):
    data = load_document_config(config)
    with DocumentIntelligenceClient(data['endpoint'], AzureKeyCredential(data['api_key'])) as client:
        return client.begin_analyze_document(model_id, body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
