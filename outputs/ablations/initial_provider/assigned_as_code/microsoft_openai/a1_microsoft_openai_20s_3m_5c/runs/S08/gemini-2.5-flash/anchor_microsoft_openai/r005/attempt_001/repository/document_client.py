import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_document_intelligence_client(config=None):
    config = config or {}
    endpoint = config.get('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT', os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'))
    api_key = config.get('AZURE_DOCUMENT_INTELLIGENCE_API_KEY', os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_API_KEY'))

    if not endpoint or not api_key:
        raise ValueError("Azure Document Intelligence endpoint and API key must be provided in config or environment variables.")

    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))
