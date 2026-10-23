"""
Local helper utilities for Azure AI Document Intelligence OCR and Layout Extraction.

Provides client initialization, configuration loading, and shared helpers
for interacting with the Azure Document Intelligence service.
"""

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


AZURE_DI_ENDPOINT_ENV = "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"
AZURE_DI_KEY_ENV = "AZURE_DOCUMENT_INTELLIGENCE_KEY"


def get_azure_di_endpoint() -> str:
    endpoint = os.environ.get(AZURE_DI_ENDPOINT_ENV)
    if not endpoint:
        raise ValueError(
            f"Missing required environment variable: {AZURE_DI_ENDPOINT_ENV}"
        )
    return endpoint


def get_azure_di_key() -> str:
    key = os.environ.get(AZURE_DI_KEY_ENV)
    if not key:
        raise ValueError(
            f"Missing required environment variable: {AZURE_DI_KEY_ENV}"
        )
    return key


def create_document_intelligence_client(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> DocumentIntelligenceClient:
    """Create an Azure AI Document Intelligence client using the azure-ai-documentintelligence SDK."""
    ep = endpoint or get_azure_di_endpoint()
    ak = key or get_azure_di_key()
    credential = AzureKeyCredential(ak)
    client = DocumentIntelligenceClient(endpoint=ep, credential=credential)
    return client


def read_file_bytes(file_path: str) -> bytes:
    """Read a local file as bytes for upload to Azure Document Intelligence."""
    with open(file_path, "rb") as fh:
        return fh.read()


def poll_analysis(poller) -> dict:
    """Wait for the long-running Azure DI analysis operation to complete and return the result dict."""
    result = poller.result()
    return result.as_dict()
