from typing import List
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from document_client import get_document_client
from document_models import TextBlock, BoundingBox, Point

def extract_layout_from_url(document_url: str) -> List[TextBlock]:
    """
    Extracts layout elements (paragraphs) from a document using Azure AI Document Intelligence.

    Args:
        document_url: The URL of the document to analyze.

    Returns:
        A list of TextBlock objects representing the document's layout.
    """
    client = get_document_client()
    poller = client.begin_analyze_document(
        "prebuilt-layout", AnalyzeDocumentRequest(url_source=document_url)
    )
    result = poller.result()

    blocks = []
    if result.paragraphs:
        for paragraph in result.paragraphs:
            if paragraph.bounding_regions:
                region = paragraph.bounding_regions[0]
                points = [Point(p.x, p.y) for p in region.polygon]
                bounding_box = BoundingBox(points=(points[0], points[1], points[2], points[3]))
                
                block = TextBlock(
                    content=paragraph.content,
                    bounding_box=bounding_box,
                    page_number=region.page_number
                )
                blocks.append(block)
    return blocks
