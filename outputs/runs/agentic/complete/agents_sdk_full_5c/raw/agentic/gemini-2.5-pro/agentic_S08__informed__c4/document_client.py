import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def get_document_client() -> DocumentIntelligenceClient:
    """
    Initializes and returns the Azure Document Intelligence client.
    
    Reads endpoint and key from environment variables:
    - AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    - AZURE_DOCUMENT_INTELLIGENCE_KEY
    
    :return: An instance of DocumentIntelligenceClient.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Document Intelligence endpoint and key must be set in environment variables."
        )

    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
