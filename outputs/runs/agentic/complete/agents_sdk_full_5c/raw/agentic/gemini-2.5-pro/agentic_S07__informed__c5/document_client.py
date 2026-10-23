import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def get_document_intelligence_client() -> DocumentIntelligenceClient:
    """
    Initializes and returns an Azure Document Intelligence client.

    Reads endpoint and key from environment variables:
    - AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    - AZURE_DOCUMENT_INTELLIGENCE_KEY

    Returns:
        An instance of DocumentIntelligenceClient.
    """
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]

    if not endpoint or not key:
        raise ValueError(
            "Azure credentials not found in environment variables."
        )

    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
