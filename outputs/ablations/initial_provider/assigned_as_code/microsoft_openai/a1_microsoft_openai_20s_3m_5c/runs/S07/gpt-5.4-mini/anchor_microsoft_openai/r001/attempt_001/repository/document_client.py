from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def load_document_config(config=None):
    config = config or {}
    return {
        'endpoint': config['endpoint'],
        'api_key': config['api_key'],
    }


def create_document_client(config):
    return DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key']))
