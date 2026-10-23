from typing import List

from document_client import get_azure_document_intelligence_client
from document_models import DocumentLayout, Block, Line


def extract_layout_from_document(document_path: str) -> DocumentLayout:
    """
    Extracts layout elements (blocks, lines) from a document using Azure Document Intelligence.
    """
    document_intelligence_client = get_azure_document_intelligence_client()

    with open(document_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", document=f
        )
    result = poller.result()

    layout = DocumentLayout()

    if result.paragraphs:
        for paragraph in result.paragraphs:
            block_lines = []
            # This is a simplification; in a real scenario, you'd map lines within the paragraph
            # For this example, we treat the whole paragraph content as one line for simplicity.
            line = Line(
                content=paragraph.content,
                confidence=paragraph.confidence,
                polygon=[
                    p
                    for point in paragraph.bounding_regions[0].polygon
                    for p in (point.x, point.y)
                ],
                words=[],
            )
            block_lines.append(line)

            block = Block(
                content=paragraph.content,
                confidence=paragraph.confidence,
                polygon=[
                    p
                    for point in paragraph.bounding_regions[0].polygon
                    for p in (point.x, point.y)
                ],
                lines=block_lines,
            )
            layout.blocks.append(block)

    if result.content:
        layout.full_text = result.content

    return layout
