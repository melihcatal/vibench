from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import os
from typing import Optional, Dict, Any


class DocumentClient:
    """
    Client helper for Azure Document Intelligence with configuration and utility methods.
    """

    def __init__(self):
        self.endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

        if not self.endpoint or not self.key:
            raise ValueError("Azure Document Intelligence credentials not configured.")

        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.key)
        )

    def get_client(self) -> DocumentIntelligenceClient:
        """Returns the configured Azure Document Intelligence client."""
        return self.client


def load_config() -> Dict[str, Any]:
    """
    Loads and validates configuration for Azure Document Intelligence.

    Returns:
        Dictionary containing configuration values.
    """
    config = {
        "endpoint": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        "key": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
    }

    if not config["endpoint"] or not config["key"]:
        raise ValueError("Azure Document Intelligence credentials not configured.")

    return config
