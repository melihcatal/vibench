import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_document_client(config=None):
    config = config or {}
    endpoint = config.get('endpoint') or os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
    api_key = config.get('api_key') or os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_API_KEY')
    if not endpoint or not api_key:
        raise ValueError('Azure Document Intelligence endpoint and api key are required')
    return DocumentIntelligenceClient(endpoint, AzureKeyCredential(api_key))


def get_model_name(name):
    return name
