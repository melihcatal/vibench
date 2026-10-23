from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import os

def get_document_client():
    """
    Initializes and returns a DocumentIntelligenceClient.
    
    Reads endpoint and key from environment variables:
    - AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    - AZURE_DOCUMENT_INTELLIGENCE_KEY
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure credentials not found in environment variables. "
            "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY."
        )

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    return client
