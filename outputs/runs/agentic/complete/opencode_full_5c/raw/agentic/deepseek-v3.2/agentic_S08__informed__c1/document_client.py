import os
from typing import Optional, Dict, Any
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError


class DocumentClient:
    """Client helper utilities for Structured Document Extraction with Azure Document Intelligence."""

    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        self.endpoint = endpoint or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.key = key or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

        if not self.endpoint or not self.key:
            raise ValueError(
                "Azure Document Intelligence credentials not configured. "
                "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables."
            )

        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.key)
        )

    def get_supported_models(self) -> Dict[str, Any]:
        """Get list of supported document models."""
        try:
            models = self.client.list_models()
            return {
                "models": [model.model_id for model in models],
                "prebuilt_models": [
                    "prebuilt-invoice",
                    "prebuilt-receipt",
                    "prebuilt-idDocument",
                    "prebuilt-businessCard",
                ],
            }
        except HttpResponseError as e:
            return {"error": str(e), "models": []}

    def validate_connection(self) -> bool:
        """Validate connection to Azure Document Intelligence service."""
        try:
            models = self.client.list_models()
            return True
        except Exception:
            return False

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {
            "azure_endpoint": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
            "azure_key_set": bool(os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")),
            "max_file_size_mb": int(os.getenv("MAX_FILE_SIZE_MB", "20")),
            "supported_formats": [".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".bmp"],
            "default_model": "prebuilt-invoice",
        }
        return config

    @staticmethod
    def prepare_document(file_path: str) -> bytes:
        """Read and prepare document for analysis."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document not found: {file_path}")

        max_size = int(os.getenv("MAX_FILE_SIZE_MB", "20")) * 1024 * 1024
        file_size = os.path.getsize(file_path)

        if file_size > max_size:
            raise ValueError(f"File size {file_size} exceeds maximum {max_size}")

        with open(file_path, "rb") as f:
            return f.read()
