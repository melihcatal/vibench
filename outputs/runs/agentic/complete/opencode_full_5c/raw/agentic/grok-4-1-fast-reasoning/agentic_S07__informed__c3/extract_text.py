import os
from document_client import create_azure_di_client, load_image_bytes
from azure.ai.documentintelligence import AnalyzeDocumentRequest
from azure.ai.documentintelligence.models import DocumentBytesSource


def extract_text(image_path: str) -> str:
    client = create_azure_di_client()
    data = load_image_bytes(image_path)
    poller = client.begin_analyze_document(
        "prebuilt-read", AnalyzeDocumentRequest(bytes_source=DocumentBytesSource(data))
    )
    result = poller.result()
    return result.content
