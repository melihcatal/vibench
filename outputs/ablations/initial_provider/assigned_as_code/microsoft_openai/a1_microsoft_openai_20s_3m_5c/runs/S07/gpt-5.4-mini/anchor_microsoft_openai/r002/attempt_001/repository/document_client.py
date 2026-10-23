import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def load_config(config=None):
    data = dict(config or {})
    data.setdefault('endpoint', os.environ['AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'])
    data.setdefault('api_key', os.environ['AZURE_DOCUMENT_INTELLIGENCE_API_KEY'])
    return data


def make_client(config=None):
    config = load_config(config)
    return DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key']))
