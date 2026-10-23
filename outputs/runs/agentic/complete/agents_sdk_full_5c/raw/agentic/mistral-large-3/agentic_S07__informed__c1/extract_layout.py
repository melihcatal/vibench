import os
from typing import List, Optional
from document_client import get_document_client
from document_models import LayoutElement, LayoutExtractionResponse


def extract_layout(image_path: str, mime_type: Optional[str] = None) -> LayoutExtractionResponse:
    """
    Extract layout elements (blocks, lines, paragraphs) from a document using Azure AI Document Intelligence.
    """
    client = get_document_client()

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        analyze_request=image_data,
        content_type="application/octet-stream"
    )
    result = poller.result()

    elements = []
    for paragraph in result.paragraphs:
        elements.append(LayoutElement(
            element_type="paragraph",
            text=paragraph.content,
            bounding_box=paragraph.bounding_regions[0].polygon if paragraph.bounding_regions else None
        ))

    for line in result.pages[0].lines:
        elements.append(LayoutElement(
            element_type="line",
            text=line.content,
            bounding_box=line.polygon
        ))

    return LayoutExtractionResponse(elements=elements)