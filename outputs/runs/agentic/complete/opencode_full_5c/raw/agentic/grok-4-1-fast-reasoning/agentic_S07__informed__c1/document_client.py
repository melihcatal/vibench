import os
import mimetypes
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult


def get_client() -> DocumentIntelligenceClient:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError(
            "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY"
        )
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def analyze_document(
    client: DocumentIntelligenceClient, model_id: str, image_path: str
) -> AnalyzeResult:
    with open(image_path, "rb") as f:
        content_type = mimetypes.guess_type(image_path)[0] or "application/octet-stream"
        poller = client.begin_analyze_document(
            model_id, document=f, content_type=content_type
        )
        poller.wait()
        result: AnalyzeResult = poller.result()
    return result
