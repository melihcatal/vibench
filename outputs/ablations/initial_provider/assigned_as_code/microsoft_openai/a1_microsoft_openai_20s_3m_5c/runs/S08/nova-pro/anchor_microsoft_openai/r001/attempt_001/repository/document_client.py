import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_document_client():
    endpoint = os.getenv('DOCUMENT_INTELLIGENCE_ENDPOINT')
    api_key = os.getenv('DOCUMENT_INTELLIGENCE_API_KEY')
    return DocumentIntelligenceClient(endpoint, AzureKeyCredential(api_key))