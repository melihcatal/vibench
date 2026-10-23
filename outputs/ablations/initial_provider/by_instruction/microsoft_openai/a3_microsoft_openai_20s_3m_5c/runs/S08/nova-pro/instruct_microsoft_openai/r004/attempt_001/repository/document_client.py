import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AzureKeyCredential

def get_document_intelligence_client():
    endpoint = os.getenv('DOCUMENT_INTELLIGENCE_ENDPOINT')
    key = os.getenv('DOCUMENT_INTELLIGENCE_KEY')
    return DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))