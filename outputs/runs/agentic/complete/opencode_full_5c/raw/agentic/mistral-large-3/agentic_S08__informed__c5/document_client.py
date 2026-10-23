import os
from typing import Optional, Dict, Any
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from mindee import Client


class DocumentClient:
    def __init__(self):
        self.azure_client = self._create_azure_client()
        self.mindee_client = self._create_mindee_client()

    def _create_azure_client(self) -> Optional[DocumentIntelligenceClient]:
        endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        if endpoint and key:
            return DocumentIntelligenceClient(
                endpoint=endpoint, credential=AzureKeyCredential(key)
            )
        return None

    def _create_mindee_client(self) -> Optional[Client]:
        api_key = os.getenv("MINDEE_API_KEY")
        if api_key:
            return Client(api_key=api_key)
        return None

    def get_azure_client(self) -> DocumentIntelligenceClient:
        if not self.azure_client:
            raise ValueError("Azure Document Intelligence client is not configured")
        return self.azure_client

    def get_mindee_client(self) -> Client:
        if not self.mindee_client:
            raise ValueError("Mindee client is not configured")
        return self.mindee_client


def load_config() -> Dict[str, Any]:
    return {
        "azure_document_intelligence": {
            "endpoint": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
            "key": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
        },
        "mindee": {"api_key": os.getenv("MINDEE_API_KEY")},
    }
