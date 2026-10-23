# [HELPER] document_client.py
"""
Local configuration and client helper utilities for Structured Document Extraction.
"""
import os
from typing import Any, Dict
from google.cloud import documentai
from azure.ai.formrecognizer import DocumentAnalysisClient
from aws_comprehend import ComprehendClient  # placeholder import

def get_processor_id(provider: str) -> str:
    """Return provider-specific processor or model ID based on env vars."""
    if provider == "google":
        return os.getenv("GOOGLE_PROCESSOR_ID", "projects/PROJECT/locations/us/processors/INVOICE_PROCESSOR")
    if provider == "azure":
        return os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT", "https://<RESOURCE>.cognitiveservices.azure.com/")
    raise ValueError("Unsupported provider")

def init_google_client() -> documentai.DocumentProcessorServiceClient:
    """Initialize Google Document AI client."""
    return documentai.DocumentProcessorServiceClient()

def init_azure_client() -> DocumentAnalysisClient:
    """
    Initialize Azure Form Recognizer client.
    Requires AZURE_ENDPOINT and AZURE_KEY env vars.
    """
    endpoint = os.getenv("AZURE_ENDPOINT", "https://<RESOURCE>.cognitiveservices.azure.com/")
    key = os.getenv("AZURE_KEY", "<YOUR_KEY>")
    return DocumentAnalysisClient(endpoint=endpoint, credential=key)

def init_validate_client() -> ComprehendClient:
    """Initialize AWS Comprehend client (used for validation)."""
    return ComprehendClient()  # uses AWS credentials from env (provider-specific)
