
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

def get_document_client() -> DocumentIntelligenceClient:
    """
    Initializes and returns an Azure Document Intelligence Client.

    Requires the following environment variables to be set:
    - AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT: The endpoint URL of the Document Intelligence resource.
    - AZURE_DOCUMENT_INTELLIGENCE_KEY: The API key for the Document Intelligence resource.
    """
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]

    if not endpoint or not key:
        raise ValueError(
            "Azure Document Intelligence endpoint and key must be set in environment variables."
        )

    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
