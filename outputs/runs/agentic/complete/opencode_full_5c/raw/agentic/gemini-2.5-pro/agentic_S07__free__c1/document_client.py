import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient


def get_document_intelligence_client():
    """
    Initializes and returns a DocumentIntelligenceClient.
    Expects environment variables:
    - DOCUMENTINTELLIGENCE_ENDPOINT: The endpoint for the Document Intelligence resource.
    - DOCUMENTINTELLIGENCE_API_KEY: The API key for the Document Intelligence resource.
    """
    endpoint = os.environ.get("DOCUMENTINTELLIGENCE_ENDPOINT")
    api_key = os.environ.get("DOCUMENTINTELLIGENCE_API_KEY")

    if not endpoint or not api_key:
        raise ValueError(
            "Azure Document Intelligence endpoint and API key must be set in environment variables."
        )

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(api_key)
    )
    return client
