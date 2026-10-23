import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import mimetypes


def get_document_intelligence_client() -> DocumentIntelligenceClient:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError(
            "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY"
        )
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def analyze_document(model_id: str, image_path: str):
    client = get_document_intelligence_client()
    content_type, _ = mimetypes.guess_type(image_path)
    if content_type is None:
        raise ValueError(f"Cannot determine content type for {image_path}")
    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id, AnalyzeDocumentRequest(f.read(), content_type)
        )
    return poller.result()
