from typing import Optional
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from azure.core.credentials import AzureKeyCredential
from document_client import get_document_intelligence_client
from document_models import TextExtractionResponse


def extract_text_from_image(image_path: str, mime_type: str = "image/jpeg") -> TextExtractionResponse:
    """Extract plain text from a scanned document image using Azure Document Intelligence."""
    client = get_document_intelligence_client()

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-read",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read()),
            content_type=mime_type
        )
    
    result: AnalyzeResult = poller.result()
    
    if not result.content:
        return TextExtractionResponse(text="", pages=[])
    
    pages = []
    for page in result.pages:
        pages.append({
            "page_number": page.page_number,
            "text": result.content
        })
    
    return TextExtractionResponse(text=result.content, pages=pages)