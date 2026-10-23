import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def load_config(config=None):
    data = dict(config or {})
    data.setdefault('endpoint', os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'))
    data.setdefault('api_key', os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_API_KEY'))
    return data


def get_document_client(config=None):
    data = load_config(config)
    return DocumentIntelligenceClient(data['endpoint'], AzureKeyCredential(data['api_key']))


def analyze_document(model_id, payload, config=None):
    data = load_config(config)
    with DocumentIntelligenceClient(data['endpoint'], AzureKeyCredential(data['api_key'])) as client:
        return client.begin_analyze_document(model_id, body=payload['document_bytes'], content_type=payload['mime_type']).result()
