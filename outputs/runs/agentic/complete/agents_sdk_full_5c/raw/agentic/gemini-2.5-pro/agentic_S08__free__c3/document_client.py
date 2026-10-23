import os
from typing import Optional

from google.api_core.client_options import ClientOptions
from google.cloud import documentai

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


def get_google_document_ai_client(
    gcp_project_id: Optional[str] = None,
    gcp_location: Optional[str] = None,
) -> documentai.DocumentProcessorServiceClient:
    """
    Returns an authenticated Google Document AI client.
    """
    project_id = gcp_project_id or os.environ["GCP_PROJECT_ID"]
    location = gcp_location or "us"  # Or your specific location
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    return documentai.DocumentProcessorServiceClient(client_options=opts)


def get_azure_document_intelligence_client(
    endpoint: Optional[str] = None, key: Optional[str] = None
) -> DocumentAnalysisClient:
    """
    Returns an authenticated Azure Document Intelligence client.
    """
    endpoint = endpoint or os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
    key = key or os.environ["AZURE_FORM_RECOGNIZER_KEY"]
    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
