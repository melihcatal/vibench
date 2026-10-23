import os
from typing import Optional, Dict, Any
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from mindee import Client


class DocumentClient:
    """
    Provides local configuration and client helper utilities for Structured Document Extraction.
    """

    @staticmethod
    def get_azure_document_intelligence_client() -> Optional[
        DocumentIntelligenceClient
    ]:
        """Initializes and returns an Azure Document Intelligence client."""
        endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

        if not endpoint or not key:
            return None

        return DocumentIntelligenceClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

    @staticmethod
    def get_mindee_client() -> Optional[Client]:
        """Initializes and returns a Mindee client."""
        api_key = os.getenv("MINDEE_API_KEY")

        if not api_key:
            return None

        return Client(api_key=api_key)

    @staticmethod
    def load_document(file_path: str) -> bytes:
        """Loads a document from the given file path."""
        with open(file_path, "rb") as f:
            return f.read()
