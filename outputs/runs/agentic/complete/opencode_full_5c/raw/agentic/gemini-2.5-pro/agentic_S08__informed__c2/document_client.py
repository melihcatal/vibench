import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient


def get_document_client() -> DocumentIntelligenceClient:
    """
    Initializes and returns a DocumentIntelligenceClient.

    Expects environment variables:
    - AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT: The endpoint for the Document Intelligence service.
    - AZURE_DOCUMENT_INTELLIGENCE_KEY: The API key for the Document Intelligence service.
    """
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure credentials not found in environment variables."
            "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY."
        )

    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
