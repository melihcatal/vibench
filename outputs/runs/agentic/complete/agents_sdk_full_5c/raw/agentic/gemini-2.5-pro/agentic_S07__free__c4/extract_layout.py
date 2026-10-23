from typing import List
from document_client import process_document
from document_models import Block, Line, BoundingPoly, Point

def _get_text(element, text: str) -> str:
    """
    Extracts text for a given element from the document's full text.
    """
    text_anchor = element.layout.text_anchor
    if not text_anchor.text_segments:
        return ""
    start_index = int(text_anchor.text_segments[0].start_index)
    end_index = int(text_anchor.text_segments[0].end_index)
    return text[start_index:end_index]

def extract_document_layout(image_content: bytes) -> List[Block]:
    """
    Extracts layout elements (blocks and lines) from a document image
    using Google Cloud Document AI.

    Args:
        image_content: The byte content of the image file.

    Returns:
        A list of Block objects representing the document's layout.
    """
    document = process_document(image_content)
    doc_text = document.text
    blocks = []

    for page in document.pages:
        for block in page.blocks:
            block_lines = []
            for line in block.lines:
                line_text = _get_text(line, doc_text)
                line_poly = BoundingPoly(
                    vertices=[Point(x=v.x, y=v.y) for v in line.layout.bounding_poly.vertices]
                )
                block_lines.append(Line(
                    text=line_text,
                    bounding_poly=line_poly,
                    confidence=line.layout.confidence
                ))

            block_text = _get_text(block, doc_text)
            block_poly = BoundingPoly(
                vertices=[Point(x=v.x, y=v.y) for v in block.layout.bounding_poly.vertices]
            )
            blocks.append(Block(
                text=block_text,
                bounding_poly=block_poly,
                confidence=block.layout.confidence,
                lines=block_lines
            ))

    return blocks
