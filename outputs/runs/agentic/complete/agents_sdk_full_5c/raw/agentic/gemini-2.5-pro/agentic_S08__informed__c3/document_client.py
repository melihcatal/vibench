import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentAnalysisClient

def get_document_client():
    """
    Initializes and returns an Azure DocumentAnalysisClient.
    """
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure credentials not found in environment variables."
        )

    return DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
