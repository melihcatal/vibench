import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentAnalysisClient

def get_document_client() -> DocumentAnalysisClient:
    """
    Retrieves an authenticated DocumentAnalysisClient.
    
    Relies on AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and 
    AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables.
    """
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]

    if not endpoint or not key:
        raise ValueError(
            "Azure Document Intelligence credentials not found in environment."
        )

    return DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
