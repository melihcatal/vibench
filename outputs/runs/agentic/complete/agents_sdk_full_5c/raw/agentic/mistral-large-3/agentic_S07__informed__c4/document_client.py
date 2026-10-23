import os
from typing import Optional, Dict, Any
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat
from azure.core.credentials import AzureKeyCredential


class DocumentClient:
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        self.endpoint = endpoint or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.key = key or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        if not self.endpoint or not self.key:
            raise ValueError(
                "Azure Document Intelligence endpoint and key must be provided or set as environment variables."
            )
        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.key)
        )

    def analyze_document(self, model_id: str, file_stream: bytes, content_type: str = "application/pdf") -> Dict[str, Any]:
        poller = self.client.begin_analyze_document(
            model_id=model_id,
            analyze_request=AnalyzeDocumentRequest(bytes_source=file_stream),
            content_type=content_type,
            output_content_format=ContentFormat.MARKDOWN,
        )
        result = poller.result()
        return result.to_dict()