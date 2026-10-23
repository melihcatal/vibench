from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def get_document_client(config):
    return DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key']))