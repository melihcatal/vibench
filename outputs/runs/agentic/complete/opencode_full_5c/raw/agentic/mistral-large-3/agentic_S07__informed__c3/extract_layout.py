from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from azure.core.credentials import AzureKeyCredential
import os
from typing import List, Dict, Optional
from document_models import LayoutElement, LayoutResponse


def extract_layout(image_path: str, mime_type: str = "image/jpeg") -> LayoutResponse:
    """
    Extracts layout elements (blocks, lines, tables) from a document using Azure Document Intelligence.

    Args:
        image_path: Path to the document image file or URL.
        mime_type: MIME type of the document (e.g., "image/jpeg", "image/png").

    Returns:
        LayoutResponse: Normalized response containing layout elements and metadata.
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
            "prebuilt-layout",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read()),
            content_type=mime_type,
        )

    result: AnalyzeResult = poller.result()

    elements = []
    for paragraph in result.paragraphs or []:
        elements.append(
            LayoutElement(
                type="paragraph",
                text=paragraph.content,
                bounding_box=paragraph.bounding_regions[0].polygon
                if paragraph.bounding_regions
                else None,
                confidence=paragraph.confidence,
            )
        )

    for table in result.tables or []:
        elements.append(
            LayoutElement(
                type="table",
                text="",
                bounding_box=table.bounding_regions[0].polygon
                if table.bounding_regions
                else None,
                confidence=table.confidence,
                rows=table.row_count,
                columns=table.column_count,
            )
        )

    return LayoutResponse(
        elements=elements, pages=len(result.pages) if result.pages else 0
    )
