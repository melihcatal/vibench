import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

def get_di_client() -> DocumentIntelligenceClient:
    endpoint = os.environ['AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT']
    key = os.environ['AZURE_DOCUMENT_INTELLIGENCE_KEY']
    return DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))
