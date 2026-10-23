from typing import List
from document_client import get_document_intelligence_client
from document_models import Block


def extract_layout_from_document(file_path: str) -> List[Block]:
    """
    Extracts layout elements (paragraphs/blocks) from a document.
    """
    document_intelligence_client = get_document_intelligence_client()

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    blocks = []
    if result.paragraphs:
        for paragraph in result.paragraphs:
            bounding_box = []
            if paragraph.bounding_regions:
                for region in paragraph.bounding_regions:
                    bounding_box.extend([(p.x, p.y) for p in region.polygon])

            blocks.append(Block(content=paragraph.content, bounding_box=bounding_box))

    return blocks
