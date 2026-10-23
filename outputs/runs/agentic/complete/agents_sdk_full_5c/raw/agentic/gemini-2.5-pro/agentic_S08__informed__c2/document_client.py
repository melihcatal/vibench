
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

def get_document_intelligence_client():
    """
    Initializes and returns a DocumentIntelligenceClient.
    
    Expects environment variables for endpoint and key.
    """
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    
    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence endpoint and key must be set in environment variables.")

    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
