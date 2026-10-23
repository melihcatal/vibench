import os

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_document_client(config=None):
    config = config or {}
    endpoint = config.get('endpoint') or os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
    api_key = config.get('api_key') or os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_KEY')
    return DocumentIntelligenceClient(endpoint, AzureKeyCredential(api_key))


def get_document_config(config=None):
    config = config or {}
    return {
        'endpoint': config.get('endpoint') or os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'),
        'api_key': config.get('api_key') or os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_KEY'),
    }
