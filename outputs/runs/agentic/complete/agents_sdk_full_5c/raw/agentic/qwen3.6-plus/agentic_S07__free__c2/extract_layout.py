"""
[SAME-SCENARIO] Extract blocks, lines, tables, and layout elements from a document.
Uses Google Cloud Document AI for advanced layout analysis including paragraphs,
tables, form fields, and visual structure detection.
"""

import os
from typing import Optional, List, Dict, Any
from google.cloud import documentai_v1
from google.cloud.documentai_v1 import DocumentProcessorServiceClient

from document_client import (
    GoogleVisionClient,
    get_vision_client,
    GOOGLE_CLOUD_PROJECT,
    GOOGLE_CLOUD_DOCUMENT_AI_ENDPOINT,
)
from document_models import (
    LayoutResponse,
    TextBlock,
    BoundingBox,
    BlockType,
    normalize_vision_vertices,
)


GOOGLE_CLOUD_DOCUMENT_AI_MODEL = "layout-parser"
GOOGLE_CLOUD_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")


class DocumentAIClient:
    """Client wrapper for Google Cloud Document AI layout parsing."""

    def __init__(
        self,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials_path: Optional[str] = None,
    ):
        self.project = project or GOOGLE_CLOUD_PROJECT
        self.location = location or GOOGLE_CLOUD_LOCATION
        self.client = DocumentProcessorServiceClient()

    def get_processor_name(self, processor_id: str) -> str:
        """Build the full processor resource name for Document AI."""
        return self.client.processor_path(
            project=self.project,
            location=self.location,
            processor=processor_id,
        )

    def process_document(
        self,
        file_path: str,
        processor_id: str,
        mime_type: str = "application/pdf",
    ) -> documentai_v1.Document:
        """Process a document using a Document AI processor."""
        processor_name = self.get_processor_name(processor_id)

        with open(file_path, "rb") as f:
            file_content = f.read()

        raw_document = documentai_v1.RawDocument(
            content=file_content,
            mime_type=mime_type,
        )

        request = documentai_v1.ProcessRequest(
            name=processor_name,
            raw_document=raw_document,
        )

        result = self.client.process_document(request=request)
        return result.document


def extract_layout_from_document(
    image_path: str,
    mime_type: str = "image/png",
    use_document_ai: bool = True,
    processor_id: Optional[str] = None,
) -> LayoutResponse:
    """
    Extract layout elements from a document using Google Cloud Document AI
    or Google Cloud Vision API as fallback.

    Uses Google's layout-parser model for paragraph, table, form, and list detection.

    Args:
        image_path: Path to the document image or PDF file.
        mime_type: MIME type of the input document.
        use_document_ai: Whether to use Document AI (True) or Vision API (False).
        processor_id: Optional Document AI processor ID.

    Returns:
        LayoutResponse containing detected blocks with types and positions.
    """
    if use_document_ai and processor_id:
        return _extract_layout_via_document_ai(image_path, processor_id, mime_type)
    else:
        return _extract_layout_via_vision_api(image_path)


def _extract_layout_via_vision_api(image_path: str) -> LayoutResponse:
    """
    Extract layout using Google Cloud Vision API with DOCUMENT_TEXT_DETECTION
    and BLOCK_TYPE detection via the builtin/latest model.
    """
    from extract_text import extract_text_from_image

    ocr_result = extract_text_from_image(image_path)

    layout_blocks = []
    for block in ocr_result.blocks:
        layout_blocks.append(
            TextBlock(
                text=block.text,
                confidence=block.confidence,
                bounding_box=block.bounding_box,
                block_type=block.block_type,
                language=block.language,
            )
        )

    return LayoutResponse(
        blocks=layout_blocks,
        page_width=1.0,
        page_height=1.0,
    )


def _extract_layout_via_document_ai(
    file_path: str,
    processor_id: str,
    mime_type: str = "application/pdf",
) -> LayoutResponse:
    """
    Extract layout using Google Cloud Document AI Document Understanding.
    Uses the documentai.googleapis.com endpoint for advanced layout parsing.
    """
    doc_ai_client = DocumentAIClient()
    document = doc_ai_client.process_document(file_path, processor_id, mime_type)

    blocks = []
    for page in document.pages:
        page_width = float(getattr(page, 'dimension', None).width if hasattr(page, 'dimension') else 1.0) or 1.0
        page_height = float(getattr(page, 'dimension', None).height if hasattr(page, 'dimension') else 1.0) or 1.0

        for block in page.blocks:
            block_text = _extract_document_ai_block_text(document, block)
            confidence = getattr(block, 'confidence', 0.0) or 0.0

            if block.layout and block.layout.bounding_poly:
                bounding_box = _extract_document_ai_bounding_box(
                    block.layout.bounding_poly, page_width, page_height
                )
            else:
                bounding_box = None

            block_type = _classify_document_ai_block(block)

            blocks.append(
                TextBlock(
                    text=block_text.strip(),
                    confidence=confidence,
                    bounding_box=bounding_box,
                    block_type=block_type,
                    language="en",
                )
            )

    return LayoutResponse(
        blocks=blocks,
        page_width=page_width,
        page_height=page_height,
    )


def _extract_document_ai_block_text(document: documentai_v1.Document, block) -> str:
    """Extract text from a Document AI block using layout token references."""
    if not block.layout or not block.layout.text_anchor:
        return ""

    text_segments = block.layout.text_anchor.text_segments
    full_text = document.text
    result_parts = []

    for segment in text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        result_parts.append(full_text[start_index:end_index])

    return "".join(result_parts)


def _extract_document_ai_bounding_box(bounding_poly, page_width: float, page_height: float) -> BoundingBox:
    """Convert Document AI bounding poly to normalized BoundingBox."""
    vertices = bounding_poly.vertices if hasattr(bounding_poly, 'vertices') else []
    x_coords = []
    y_coords = []

    for vertex in vertices:
        if hasattr(vertex, 'x'):
            x_coords.append(float(vertex.x) / page_width if page_width > 0 else 0)
        if hasattr(vertex, 'y'):
            y_coords.append(float(vertex.y) / page_height if page_height > 0 else 0)

    if not x_coords or not y_coords:
        return BoundingBox(0.0, 0.0, 1.0, 1.0)

    return BoundingBox(
        x_min=min(x_coords),
        y_min=min(y_coords),
        x_max=max(x_coords),
        y_max=max(y_coords),
    )


def _classify_document_ai_block(block) -> BlockType:
    """Classify a Document AI block into a BlockType enum."""
    block_type_str = getattr(block, 'block_type', None)
    if block_type_str is not None:
        type_map = {
            documentai_v1.Document.Page.Block.BlockType.TEXT: BlockType.TEXT,
            documentai_v1.Document.Page.Block.BlockType.TABLE: BlockType.TABLE,
            documentai_v1.Document.Page.Block.BlockType.FORM: BlockType.FORM,
            documentai_v1.Document.Page.Block.BlockType.LIST: BlockType.LIST_ITEM,
            documentai_v1.Document.Page.Block.BlockType.IMAGE: BlockType.IMAGE,
            documentai_v1.Document.Page.Block.BlockType.BARCODE: BlockType.BARCODE,
            documentai_v1.Document.Page.Block.BlockType.UNDEFINED: BlockType.TEXT,
        }
        return type_map.get(block_type_str, BlockType.TEXT)

    return BlockType.TEXT


if __name__ == "__main__":
    doc_path = os.environ.get("DOCUMENT_PATH", "sample_document.pdf")
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID", "layout-processor")
    result = extract_layout_from_document(doc_path, processor_id=processor_id)
    for block in result.blocks:
        print(f"[{block.block_type.value}] {block.text[:80]}...")
