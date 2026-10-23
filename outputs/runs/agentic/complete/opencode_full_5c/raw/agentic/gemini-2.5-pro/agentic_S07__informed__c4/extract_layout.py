from typing import List
from document_client import DocumentAIClient
from document_models import DocumentLayout, Block, Line, BoundingBox


def _get_bounding_box(bounding_poly) -> BoundingBox:
    if not bounding_poly or not bounding_poly.normalized_vertices:
        return BoundingBox(0, 0, 0, 0)

    vertices = bounding_poly.normalized_vertices
    return BoundingBox(
        x1=vertices[0].x, y1=vertices[0].y, x2=vertices[2].x, y2=vertices[2].y
    )


def extract_layout_from_document(file_path: str) -> DocumentLayout:
    """
    Extracts blocks, lines, tables, or layout elements from a document.
    """
    client = DocumentAIClient()
    document = client.process_document(file_path)

    blocks = []
    lines = []

    for page in document.pages:
        for block in page.blocks:
            blocks.append(
                Block(
                    text="".join(
                        [
                            document.text[
                                int(segment.start_index) : int(segment.end_index)
                            ]
                            for segment in block.layout.text_anchor.text_segments
                        ]
                    ),
                    confidence=block.layout.confidence,
                    bounding_box=_get_bounding_box(block.layout.bounding_poly),
                )
            )
        for line in page.lines:
            lines.append(
                Line(
                    text="".join(
                        [
                            document.text[
                                int(segment.start_index) : int(segment.end_index)
                            ]
                            for segment in line.layout.text_anchor.text_segments
                        ]
                    ),
                    confidence=line.layout.confidence,
                    bounding_box=_get_bounding_box(line.layout.bounding_poly),
                )
            )

    return DocumentLayout(text=document.text, blocks=blocks, lines=lines, tables=[])
