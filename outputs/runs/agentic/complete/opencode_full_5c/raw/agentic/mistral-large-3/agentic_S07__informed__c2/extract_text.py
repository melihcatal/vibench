from typing import Dict, List, Optional
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import (
    AnalyzeDocumentRequest,
    AnalyzeResult,
    ParagraphRole,
)
from azure.core.credentials import AzureKeyCredential


def extract_text(image_path: str) -> str:
    """
    Extracts plain text from a scanned document image using Azure Document Intelligence.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence credentials not configured.")

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-read",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read()),
        )

    result: AnalyzeResult = poller.result()

    text = ""
    if result.paragraphs:
        for paragraph in result.paragraphs:
            if paragraph.role == ParagraphRole.TITLE:
                text += f"\n{paragraph.content}\n"
            else:
                text += f"{paragraph.content} "

    return text.strip()
