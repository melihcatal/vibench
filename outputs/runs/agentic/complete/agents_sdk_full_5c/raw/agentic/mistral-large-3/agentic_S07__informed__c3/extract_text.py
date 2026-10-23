from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat
from azure.core.credentials import AzureKeyCredential
import os

from document_client import get_document_intelligence_client
from document_models import OCRTextResponse


def extract_text_from_image(image_path: str) -> OCRTextResponse:
    client = get_document_intelligence_client()

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-read",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read()),
            content_format=ContentFormat.TEXT
        )

    result = poller.result()

    return OCRTextResponse(
        text=result.content,
        pages=[
            {
                "page_number": page.page_number,
                "lines": [line.content for line in page.lines] if page.lines else []
            }
            for page in result.pages
        ]
    )