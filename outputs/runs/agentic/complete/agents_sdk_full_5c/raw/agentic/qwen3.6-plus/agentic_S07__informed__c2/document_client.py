"""
Local configuration and client helper utilities for OCR and Layout Extraction.
Provides Azure AI Document Intelligence client initialization and helper functions.
"""

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_azure_endpoint() -> str:
    """Retrieve Azure Document Intelligence endpoint from environment."""
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    if not endpoint:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT environment variable is required"
        )
    return endpoint


def get_azure_key() -> str:
    """Retrieve Azure Document Intelligence API key from environment."""
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_KEY environment variable is required"
        )
    return key


def create_document_client() -> DocumentIntelligenceClient:
    """
    Create and return an Azure AI Document Intelligence client.

    Returns:
        DocumentIntelligenceClient: Authenticated client for Azure Document Intelligence.
    """
    endpoint = get_azure_endpoint()
    key = get_azure_key()
    credential = AzureKeyCredential(key)
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=credential)
    return client


def read_image_bytes(file_path: str) -> bytes:
    """Read an image file and return its binary content."""
    with open(file_path, "rb") as f:
        return f.read()


def normalize_azure_poller_response(poller) -> dict:
    """
    Wait for Azure Document Intelligence operation to complete and return result.

    Args:
        poller: Azure LRO poller object from begin_analyze_document.

    Returns:
        dict: The completed analyze result dictionary.
    """
    result = poller.result()
    return result
