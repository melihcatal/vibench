import os
from typing import Optional, Dict, Any
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


class DocumentClient:
    """
    Client helper for Azure Document Intelligence.
    """

    def __init__(self):
        self.endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

        if not self.endpoint or not self.key:
            raise ValueError("Azure Document Intelligence credentials not configured.")

        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.key)
        )

    def analyze_document(self, model_id: str, file_path: str) -> Any:
        """
        Analyze a document using the specified model.
        """
        with open(file_path, "rb") as f:
            poller = self.client.begin_analyze_document(
                model_id=model_id, analyze_request={"bytes_source": f.read()}
            )
        return poller.result()


def load_config() -> Dict[str, str]:
    """
    Load configuration for Azure Document Intelligence.
    """
    return {
        "endpoint": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        "key": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
    }
