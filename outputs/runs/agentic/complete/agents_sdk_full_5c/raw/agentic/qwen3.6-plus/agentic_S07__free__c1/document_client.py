"""
Local configuration and client helper utilities for OCR and Layout Extraction.

Provides configuration loading, image preprocessing, API credential management,
and shared client initialization utilities for Azure AI Document Intelligence
and related providers.
"""

import base64
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from document_models import ImageSource


class AzureDocumentClient:
    """
    Client helper for Azure AI Document Intelligence (formerly Form Recognizer).
    Uses the azure-ai-formrecognizer SDK.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 120,
    ):
        self.endpoint = endpoint or os.environ.get(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", ""
        )
        self.api_key = api_key or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
        self.timeout = timeout

    def get_credential(self) -> "AzureKeyCredential":
        """Return an Azure key credential for the SDK client."""
        from azure.core.credentials import AzureKeyCredential
        return AzureKeyCredential(self.api_key)

    def create_document_analysis_client(self) -> "DocumentAnalysisClient":
        """Create and return a DocumentAnalysisClient from azure-ai-formrecognizer."""
        from azure.ai.formrecognizer import DocumentAnalysisClient
        return DocumentAnalysisClient(
            endpoint=self.endpoint,
            credential=self.get_credential(),
        )

    @staticmethod
    def encode_image_to_base64(file_path: str) -> Tuple[str, str]:
        """
        Read an image file and return (base64_string, content_type).
        """
        path = Path(file_path)
        content = path.read_bytes()
        encoded = base64.b64encode(content).decode("utf-8")
        suffix = path.suffix.lower()
        content_type_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".tiff": "image/tiff",
            ".tif": "image/tiff",
            ".bmp": "image/bmp",
            ".pdf": "application/pdf",
        }
        content_type = content_type_map.get(suffix, "image/png")
        return encoded, content_type


def prepare_image_source(
    file_path: Optional[str] = None,
    base64_data: Optional[str] = None,
    content_type: str = "image/png",
) -> ImageSource:
    """
    Prepare an ImageSource from either a file path or raw base64 data.
    """
    if file_path and Path(file_path).exists():
        encoded, ct = AzureDocumentClient.encode_image_to_base64(file_path)
        return ImageSource(
            file_path=file_path,
            base64_data=encoded,
            content_type=ct,
            mime_type=ct,
        )
    if base64_data:
        return ImageSource(
            base64_data=base64_data,
            content_type=content_type,
            mime_type=content_type,
        )
    raise ValueError("Either file_path or base64_data must be provided.")


def get_azure_client() -> AzureDocumentClient:
    """
    Factory helper to create a configured AzureDocumentClient from environment.
    """
    return AzureDocumentClient()


def load_document_config() -> Dict[str, Any]:
    """
    Load document processing configuration from environment variables.
    Returns a dict with provider settings, model IDs, timeouts, etc.
    """
    return {
        "provider": "azure",
        "endpoint": os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", ""),
        "api_key": os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", ""),
        "timeout": int(os.environ.get("DOCUMENT_INTELLIGENCE_TIMEOUT", "120")),
        "language": os.environ.get("DOCUMENT_OCR_LANGUAGE", "en"),
        "model_id": os.environ.get("DOCUMENT_MODEL_ID", "prebuilt-read"),
        "layout_model_id": os.environ.get("DOCUMENT_LAYOUT_MODEL_ID", "prebuilt-layout"),
        "table_model_id": os.environ.get("DOCUMENT_TABLE_MODEL_ID", "prebuilt-layout"),
    }
