# document_client.py
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

def get_document_intelligence_client() -> DocumentIntelligenceClient:
    """
    Initializes and returns a DocumentIntelligenceClient.
    
    Expects the following environment variables to be set:
    - AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT: The endpoint for the Document Intelligence resource.
    - AZURE_DOCUMENT_INTELLIGENCE_KEY: The key for the Document Intelligence resource.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Document Intelligence endpoint and key must be set as environment variables."
        )

    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
