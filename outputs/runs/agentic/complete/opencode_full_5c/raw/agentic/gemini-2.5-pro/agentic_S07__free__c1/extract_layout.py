from typing import List
from document_client import get_document_intelligence_client
from document_models import Block, BoundingRegion, Point, Span


def extract_layout(image_path: str) -> List[Block]:
    """
    Extracts layout elements (paragraphs/blocks) from a document.
    """
    client = get_document_intelligence_client()

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    layout_blocks = []
    if result.paragraphs:
        for paragraph in result.paragraphs:
            regions = []
            if paragraph.bounding_regions:
                for region in paragraph.bounding_regions:
                    points = [Point(x=p.x, y=p.y) for p in region.polygon]
                    regions.append(
                        BoundingRegion(page_number=region.page_number, polygon=points)
                    )

            spans = [Span(offset=s.offset, length=s.length) for s in paragraph.spans]

            block = Block(
                content=paragraph.content, bounding_regions=regions, spans=spans
            )
            layout_blocks.append(block)

    return layout_blocks
