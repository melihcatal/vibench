"""
extract_layout.py - Extracts blocks, lines, tables, or layout elements from a document
using Azure AI Document Intelligence (prebuilt-layout model).

Provider: Azure AI Document Intelligence
SDK: azure-ai-formrecognizer
Model: prebuilt-layout
"""

from typing import List

from document_client import get_azure_client
from document_models import (
    BoundingBox,
    ExtractLayoutRequest,
    ExtractLayoutResponse,
    LayoutElement,
    normalize_bbox_from_vertices,
)

PROVIDER = "azure"
AZURE_MODEL_ID = "prebuilt-layout"


def _bbox_from_region(region) -> BoundingBox:
    """Convert an Azure bounding region to a normalized BoundingBox."""
    if hasattr(region, "bounding_box") and region.bounding_box:
        bb = region.bounding_box
        return BoundingBox(
            x=bb[0] if len(bb) > 0 else 0.0,
            y=bb[1] if len(bb) > 1 else 0.0,
            width=(bb[2] - bb[0]) if len(bb) > 2 else 0.0,
            height=(bb[3] - bb[1]) if len(bb) > 3 else 0.0,
        )
    return BoundingBox()


def _bbox_from_polygon(polygon) -> BoundingBox:
    """Convert a polygon to a normalized BoundingBox."""
    if not polygon:
        return BoundingBox()
    vertices = [{"x": p.x, "y": p.y} for p in polygon]
    return normalize_bbox_from_vertices(vertices)


def extract_layout(request: ExtractLayoutRequest) -> ExtractLayoutResponse:
    """
    Extract layout elements (blocks, lines, words, tables, selection marks)
    from a document image using Azure AI Document Intelligence's
    prebuilt-layout model.

    Args:
        request: ExtractLayoutRequest with image source and feature flags.

    Returns:
        ExtractLayoutResponse containing a list of LayoutElement objects.
    """
    from io import BytesIO
    import base64

    if request.image.base64_data is None:
        raise ValueError("Image base64_data is required for layout extraction.")

    image_bytes = BytesIO(base64.b64decode(request.image.base64_data))

    client = get_azure_client()
    analysis_client = client.create_document_analysis_client()

    poller = analysis_client.begin_analyze_document(
        model_id=AZURE_MODEL_ID,
        document=image_bytes,
    )
    result = poller.result()

    all_elements: List[LayoutElement] = []
    page_width = 0
    page_height = 0
    overall_confidence = 0.0

    for page in result.pages:
        if hasattr(page, "width"):
            page_width = max(page_width, page.width or 0)
        if hasattr(page, "height"):
            page_height = max(page_height, page.height or 0)

        if "blocks" in request.features or "paragraphs" in request.features:
            if hasattr(page, "paragraphs") and page.paragraphs:
                for para in page.paragraphs:
                    bbox = _bbox_from_polygon(
                        getattr(para, "bounding_polygon", None)
                    )
                    element = LayoutElement(
                        element_type="paragraph",
                        text=para.content if hasattr(para, "content") else "",
                        confidence=para.confidence if hasattr(para, "confidence") else 0.0,
                        bounding_box=bbox,
                    )
                    all_elements.append(element)

        if "lines" in request.features:
            if hasattr(page, "lines") and page.lines:
                for line in page.lines:
                    bbox = _bbox_from_polygon(
                        getattr(line, "bounding_polygon", None)
                    )
                    element = LayoutElement(
                        element_type="line",
                        text=line.content if hasattr(line, "content") else "",
                        confidence=line.confidence if hasattr(line, "confidence") else 0.0,
                        bounding_box=bbox,
                    )
                    all_elements.append(element)

        if "words" in request.features:
            if hasattr(page, "words") and page.words:
                for word in page.words:
                    bbox = _bbox_from_polygon(
                        getattr(word, "bounding_polygon", None)
                    )
                    element = LayoutElement(
                        element_type="word",
                        text=word.content,
                        confidence=word.confidence,
                        bounding_box=bbox,
                    )
                    all_elements.append(element)

        if "tables" in request.features:
            if hasattr(page, "tables") and page.tables:
                for table in page.tables:
                    bbox = _bbox_from_region(
                        table.bounding_regions[0] if table.bounding_regions else None
                    )
                    element = LayoutElement(
                        element_type="table",
                        text=f"[Table: {table.row_count} rows x {table.column_count} cols]",
                        confidence=table.confidence if hasattr(table, "confidence") else 0.0,
                        bounding_box=bbox,
                    )
                    all_elements.append(element)

        if "selection_marks" in request.features:
            if hasattr(page, "selection_marks") and page.selection_marks:
                for mark in page.selection_marks:
                    bbox = _bbox_from_polygon(
                        getattr(mark, "bounding_polygon", None)
                    )
                    element = LayoutElement(
                        element_type="selection_mark",
                        text=mark.state if hasattr(mark, "state") else "unknown",
                        confidence=mark.confidence if hasattr(mark, "confidence") else 0.0,
                        bounding_box=bbox,
                    )
                    all_elements.append(element)

    if all_elements:
        overall_confidence = sum(
            e.confidence for e in all_elements if e.confidence > 0
        ) / len([e for e in all_elements if e.confidence > 0])

    return ExtractLayoutResponse(
        elements=all_elements,
        page_width=page_width,
        page_height=page_height,
        confidence=overall_confidence,
        provider=PROVIDER,
        raw_response={"status": "success", "model_id": AZURE_MODEL_ID},
    )


def extract_layout_from_file(file_path: str) -> ExtractLayoutResponse:
    """
    Convenience function to extract layout elements directly from a file path.

    Args:
        file_path: Path to the document image file.

    Returns:
        ExtractLayoutResponse with layout elements.
    """
    from document_client import prepare_image_source

    image_source = prepare_image_source(file_path=file_path)
    req = ExtractLayoutRequest(
        image=image_source,
        features=["blocks", "lines", "words", "tables", "selection_marks"],
    )
    return extract_layout(req)
