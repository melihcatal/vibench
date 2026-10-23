"""
Local configuration and client helper utilities for Structured Document Extraction.

Provides Azure AI Document Intelligence client initialization and configuration
for invoice and receipt field extraction.

Provider: Azure AI Document Intelligence (Form Recognizer)
Endpoint: https://{resource-name}.cognitiveservices.azure.com
SDK: azure-ai-documentintelligence
"""

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "https://your-resource.cognitiveservices.azure.com/",
)
DOCUMENT_INTELLIGENCE_KEY = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_KEY", ""
)


def get_document_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> DocumentIntelligenceClient:
    """
    Initialize and return an Azure AI Document Intelligence client.

    Args:
        endpoint: Azure Document Intelligence endpoint URL.
                  Default: AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT env var.
        api_key: Azure Document Intelligence API key.
                 Default: AZURE_DOCUMENT_INTELLIGENCE_KEY env var.

    Returns:
        DocumentIntelligenceClient instance configured for document analysis.
    """
    ep = endpoint or DOCUMENT_INTELLIGENCE_ENDPOINT
    key = api_key or DOCUMENT_INTELLIGENCE_KEY

    if not ep or not key:
        raise ValueError(
            "Azure Document Intelligence credentials are required. "
            "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY."
        )

    credential = AzureKeyCredential(key)
    client = DocumentIntelligenceClient(
        endpoint=ep,
        credential=credential,
    )
    return client


def get_analysis_client_for_prebuilt(
    model_id: str = "prebuilt-invoice",
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> tuple[DocumentIntelligenceClient, str]:
    """
    Get a configured client and the model ID for prebuilt document analysis.

    Args:
        model_id: Prebuilt model identifier (e.g., 'prebuilt-invoice', 'prebuilt-receipt').
        endpoint: Azure Document Intelligence endpoint URL.
        api_key: Azure Document Intelligence API key.

    Returns:
        Tuple of (DocumentIntelligenceClient, model_id).
    """
    client = get_document_client(endpoint=endpoint, api_key=api_key)
    return client, model_id


def build_analysis_request(
    file_path: str,
    content_type: Optional[str] = None,
) -> tuple[bytes, Optional[str]]:
    """
    Read a document file and prepare it for Azure Document Intelligence analysis.

    Args:
        file_path: Path to the document file (PDF, image, etc.).
        content_type: MIME type of the document. Auto-detected if None.

    Returns:
        Tuple of (file_bytes, content_type).
    """
    if content_type is None:
        ext = os.path.splitext(file_path)[1].lower()
        content_type_map = {
            ".pdf": "application/pdf",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".tiff": "image/tiff",
            ".bmp": "image/bmp",
        }
        content_type = content_type_map.get(ext, "application/octet-stream")

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    return file_bytes, content_type
