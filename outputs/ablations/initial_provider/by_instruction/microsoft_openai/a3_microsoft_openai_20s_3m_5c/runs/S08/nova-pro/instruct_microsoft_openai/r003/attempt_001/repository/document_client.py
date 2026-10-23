import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

# Initialize the client
def get_document_intelligence_client():
    endpoint = os.getenv('DOCUMENT_INTELLIGENCE_ENDPOINT')
    key = os.getenv('DOCUMENT_INTELLIGENCE_KEY')
    credential = AzureKeyCredential(key)
    client = DocumentIntelligenceClient(endpoint, credential)
    return client