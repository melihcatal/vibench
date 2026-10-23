"""
extract_text.py - Extracts plain text from a scanned document image
using Azure AI Document Intelligence (prebuilt-read model).

Provider: Azure AI Document Intelligence
SDK: azure-ai-formrecognizer
Model: prebuilt-read
"""

from typing import Optional

from document_client import get_azure_client
from document_models import (
    BoundingBox,
    ExtractTextRequest,
    ExtractTextResponse,
    OCRBlock,
    OCRLine,
    OCRWord,
    normalize_bbox_from_vertices,
)

PROVIDER = "azure"
AZURE_MODEL_ID = "prebuilt-read"


def extract_text(request: ExtractTextRequest) -> ExtractTextResponse:
    """
    Extract plain text from a scanned document image using Azure
    AI Document Intelligence's prebuilt-read OCR model.

    Args:
        request: ExtractTextRequest with image source and optional language hints.

    Returns:
        ExtractTextResponse containing full_text, blocks, lines, and words.
    """
    if request.image.base64_data is None:
        raise ValueError("Image base64_data is required for extraction.")

    from io import BytesIO
    import base64

    image_bytes = BytesIO(base64.b64decode(request.image.base64_data))
    mime_type = request.image.mime_type or request.image.content_type

    client = get_azure_client()
    analysis_client = client.create_document_analysis_client()

    poller = analysis_client.begin_analyze_document(
        model_id=AZURE_MODEL_ID,
        document=image_bytes,
        locale=request.language_hints[0] if request.language_hints else None,
    )
    result = poller.result()

    full_text_parts = []
    all_blocks = []
    all_lines = []
    all_words = []

    for page in result.pages:
        page_words = []
        page_lines = []
        page_blocks = []

        if page.words:
            for word in page.words:
                vertices = (
                    [
                        {"x": p.x, "y": p.y}
                        for p in word.bounding_polygon or []
                    ]
                    if word.bounding_polygon
                    else None
                )
                bbox = normalize_bbox_from_vertices(vertices) if vertices else None
                ocr_word = OCRWord(
                    text=word.content,
                    confidence=word.confidence,
                    bounding_box=bbox,
                )
                page_words.append(ocr_word)
                all_words.append(ocr_word)

        if page.lines:
            for line in page.lines:
                word_list = []
                if hasattr(line, "spans") and page_words:
                    offset = line.spans[0].offset if line.spans else 0
                    length = line.spans[0].length if line.spans else 0
                    line_text = result.content[offset: offset + length] if result.content else ""
                else:
                    line_text = line.content if hasattr(line, "content") else ""

                vertices = (
                    [
                        {"x": p.x, "y": p.y}
                        for p in line.bounding_polygon or []
                    ]
                    if line.bounding_polygon
                    else None
                )
                bbox = normalize_bbox_from_vertices(vertices) if vertices else None

                ocr_line = OCRLine(
                    text=line_text,
                    confidence=line.confidence,
                    words=word_list,
                    bounding_box=bbox,
                )
                page_lines.append(ocr_line)
                all_lines.append(ocr_line)

        if hasattr(page, "paragraphs") and page.paragraphs:
            for para in page.paragraphs:
                para_text = para.content if hasattr(para, "content") else ""
                bbox = None
                if hasattr(para, "bounding_regions") and para.bounding_regions:
                    bbox = BoundingBox(
                        x=para.bounding_regions[0].bounding_box[0]
                        if hasattr(para.bounding_regions[0], "bounding_box")
                        else 0,
                        y=0,
                        width=0,
                        height=0,
                    )
                block = OCRBlock(
                    text=para_text,
                    block_type="paragraph",
                    confidence=para.confidence if hasattr(para, "confidence") else 0.0,
                    bounding_box=bbox,
                )
                page_blocks.append(block)
                all_blocks.append(block)

        if result.content:
            full_text_parts.append(result.content)

    full_text = "\n".join(full_text_parts) if full_text_parts else ""

    return ExtractTextResponse(
        full_text=full_text,
        blocks=all_blocks,
        lines=all_lines,
        words=all_words,
        page_count=len(result.pages) if result.pages else 0,
        provider=PROVIDER,
        raw_response={"status": "success", "model_id": AZURE_MODEL_ID},
    )


def extract_text_from_file(file_path: str, language: Optional[str] = None) -> ExtractTextResponse:
    """
    Convenience function to extract text directly from a file path.

    Args:
        file_path: Path to the document image file.
        language: Optional language hint (e.g., 'en', 'fr').

    Returns:
        ExtractTextResponse with extracted text and metadata.
    """
    from document_client import prepare_image_source

    image_source = prepare_image_source(file_path=file_path)
    req = ExtractTextRequest(
        image=image_source,
        language_hints=[language] if language else [],
    )
    return extract_text(req)
