from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def get_document_client(endpoint, api_key):
    return DocumentIntelligenceClient(endpoint, AzureKeyCredential(api_key))