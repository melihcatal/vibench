from typing import List
from document_client import get_document_client
from document_models import DocumentLayoutBlock


def extract_layout_from_document(file_path: str) -> List[DocumentLayoutBlock]:
    document_intelligence_client = get_document_client()

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    layout_blocks = []
    if result.paragraphs:
        for paragraph in result.paragraphs:
            bounding_box = []
            if paragraph.bounding_regions:
                for region in paragraph.bounding_regions:
                    bounding_box.extend(region.polygon)

            layout_blocks.append(
                DocumentLayoutBlock(
                    content=paragraph.content,
                    page_number=paragraph.bounding_regions[0].page_number
                    if paragraph.bounding_regions
                    else 0,
                    bounding_box=bounding_box,
                )
            )
    return layout_blocks
