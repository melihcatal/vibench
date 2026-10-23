
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

def get_document_intelligence_client():
    """
    Initializes and returns a DocumentIntelligenceClient.
    
    Reads endpoint and key from environment variables:
    - AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    - AZURE_DOCUMENT_INTELLIGENCE_KEY
    """
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]

    if not endpoint or not key:
        raise ValueError("Azure credentials (endpoint and key) are not set in environment variables.")

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    return client
