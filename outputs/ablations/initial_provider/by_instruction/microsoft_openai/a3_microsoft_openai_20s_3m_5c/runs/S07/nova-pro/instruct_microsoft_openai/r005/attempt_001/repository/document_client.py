import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def get_document_client():
    return DocumentIntelligenceClient(endpoint=os.getenv('DOCUMENTINTELLIGENCE_ENDPOINT'), credential=AzureKeyCredential(os.getenv('DOCUMENTINTELLIGENCE_API_KEY')))
