import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def get_document_client():
    return DocumentIntelligenceClient(
        os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'),
        AzureKeyCredential(os.getenv('AZURE_DOCUMENT_INTELLIGENCE_API_KEY'))
    )