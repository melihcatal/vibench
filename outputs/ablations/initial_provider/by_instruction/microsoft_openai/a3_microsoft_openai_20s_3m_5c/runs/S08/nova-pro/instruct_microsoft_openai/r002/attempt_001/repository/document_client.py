import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def get_document_client():
    endpoint = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("DOCUMENT_INTELLIGENCE_KEY")
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))