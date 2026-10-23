import os
from typing import Optional, Dict, Any
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat
from azure.core.credentials import AzureKeyCredential


class DocumentClient:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        self.client = self._create_client()

    def _create_client(self) -> DocumentIntelligenceClient:
        if not self.endpoint or not self.key:
            raise ValueError(
                "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY must be set"
            )
        return DocumentIntelligenceClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.key)
        )

    def analyze_document(self, file_path: str, model_id: str = "prebuilt-layout") -> Dict[str, Any]:
        with open(file_path, "rb") as f:
            poller = self.client.begin_analyze_document(
                model_id=model_id,
                analyze_request=AnalyzeDocumentRequest(bytes_source=f),
                content_type="application/octet-stream",
                output_content_format=ContentFormat.MARKDOWN,
            )
        return poller.result().to_dict()