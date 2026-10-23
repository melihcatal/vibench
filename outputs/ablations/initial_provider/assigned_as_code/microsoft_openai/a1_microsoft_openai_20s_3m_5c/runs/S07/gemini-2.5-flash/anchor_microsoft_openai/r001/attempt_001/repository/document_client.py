from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def get_document_intelligence_client(endpoint: str, api_key: str) -> DocumentIntelligenceClient:
    return DocumentIntelligenceClient(endpoint, AzureKeyCredential(api_key))
