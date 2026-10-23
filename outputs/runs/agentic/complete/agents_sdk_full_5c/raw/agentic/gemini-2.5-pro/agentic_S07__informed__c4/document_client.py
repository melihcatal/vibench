import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentAnalysisClient


def get_document_client() -> DocumentAnalysisClient:
    """
    Creates and returns a DocumentAnalysisClient authenticated using environment variables.
    """
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]

    if not endpoint or not key:
        raise ValueError(
            "Azure credentials not found in environment variables."
            "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY."
        )

    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
