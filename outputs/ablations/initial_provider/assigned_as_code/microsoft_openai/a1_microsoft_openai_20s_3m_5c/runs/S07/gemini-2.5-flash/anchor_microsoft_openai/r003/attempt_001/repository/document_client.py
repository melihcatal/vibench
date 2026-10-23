import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def get_document_intelligence_client():
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    api_key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_API_KEY")
    if not endpoint or not api_key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_API_KEY must be set in environment variables.")
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))
