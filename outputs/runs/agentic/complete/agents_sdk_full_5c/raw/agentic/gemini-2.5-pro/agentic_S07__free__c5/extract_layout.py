# extract_layout.py
from typing import List
from document_client import get_document_intelligence_client
from document_models import ExtractedLayout, LayoutElement, BoundingBox

def extract_layout_from_url(document_url: str) -> ExtractedLayout:
    """
    Extracts layout elements (paragraphs, headings) from a document image
    using Azure AI Document Intelligence's "prebuilt-layout" model.
    """
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-layout", analyze_request={"urlSource": document_url}
    )
    result = poller.result()

    elements: List[LayoutElement] = []
    if result.paragraphs:
        for paragraph in result.paragraphs:
            bounding_regions = paragraph.bounding_regions
            box = BoundingBox(points=[
                {"x": p.x, "y": p.y} for p in bounding_regions[0].polygon
            ]) if bounding_regions else BoundingBox(points=[])
            
            elements.append(
                LayoutElement(
                    type=paragraph.role or "paragraph",
                    content=paragraph.content,
                    bounding_box=box,
                )
            )

    return ExtractedLayout(elements=elements, source_url=document_url)
