import os
from azure.ai.documentintelligence import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

def get_document_intelligence_client() -> DocumentAnalysisClient:
    """
    Provides a configured Azure Document Intelligence client.
    """
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY must be set in environment variables.")

    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_google_project_id() -> str:
    """
    Provides the Google Cloud Project ID from environment variables.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    return project_id
