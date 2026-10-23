"""
Extracts blocks, lines, tables, and layout elements from a document using AWS Textract.

Provider: AWS Textract (AnalyzeDocument API with LAYOUT feature)
Model/Feature: AWS Textract AnalyzeDocument with LAYOUT feature type
"""

import os
from typing import List

from document_client import (
    create_textract_client,
    load_image_bytes,
    build_textract_image_payload,
    normalize_textract_response,
)
from document_models import LayoutResponse, LayoutElement


# AWS Textract AnalyzeDocument layout model identifier
TEXTRACT_LAYOUT_MODEL = "aws-textract-analyze-document-layout"

# Textract-specific layout feature type
TEXTRACT_LAYOUT_FEATURES = ["LAYOUT"]

# Textract layout block types to extract
LAYOUT_BLOCK_TYPES = [
    "LAYOUT_TEXT",
    "LAYOUT_FIGURE",
    "LAYOUT_TABLE",
    "LAYOUT_LIST",
    "LAYOUT_HEADER",
    "LAYOUT_FOOTER",
    "LAYOUT_PAGE_NUMBER",
    "LAYOUT_SECTION_NAME",
    "LAYOUT_TITLE",
    "LAYOUT_KEY_VALUE",
    "LAYOUT_PICTURE",
]


def extract_layout_from_image(image_path: str) -> LayoutResponse:
    """
    Extract layout elements from a document image using AWS Textract AnalyzeDocument.

    Uses Textract's LAYOUT feature to identify document structure including
    text regions, figures, tables, lists, headers, footers, titles, and sections.

    Args:
        image_path: Path to the document image file

    Returns:
        LayoutResponse containing all detected layout elements
    """
    client = create_textract_client()
    image_bytes = load_image_bytes(image_path)
    payload = build_textract_image_payload(image_bytes)

    # AWS Textract AnalyzeDocument with LAYOUT feature
    response = client.analyze_document(
        Document=payload,
        FeatureTypes=["LAYOUT"]
    )

    normalized = normalize_textract_response(response)
    elements = _parse_layout_elements(normalized["blocks"])

    page_blocks = [b for b in normalized["blocks"] if b.get("BlockType") == "PAGE"]
    page_count = max(len(page_blocks), 1)

    return LayoutResponse(
        elements=elements,
        page_count=page_count,
        model_version=normalized.get("model_version", TEXTRACT_LAYOUT_MODEL),
        status_code=normalized.get("status_code", 0),
    )


def _parse_layout_elements(blocks: List[dict]) -> List[LayoutElement]:
    """
    Parse Textract layout blocks into normalized LayoutElement objects.

    Args:
        blocks: List of Textract Block dictionaries

    Returns:
        List of LayoutElement objects
    """
    elements = []

    for block in blocks:
        block_type = block.get("BlockType", "")
        text = block.get("Text", "")

        # Process standard Textract layout element types
        if block_type in LAYOUT_BLOCK_TYPES:
            relationships = block.get("Relationships", [])
            geometry = block.get("Geometry", {})

            # Extract child text from relationships if available
            if not text and relationships:
                text = _extract_relationship_text(blocks, relationships)

            element = LayoutElement(
                element_type=block_type,
                text=text.strip(),
                confidence=block.get("Confidence", 0.0),
                bounding_box=geometry.get("BoundingBox", {}),
                page=block.get("Page", 0),
                relationships=relationships,
            )
            elements.append(element)

        # Also capture LINE and WORD blocks within layout context
        elif block_type in ("LINE", "WORD", "TABLE", "CELL"):
            geometry = block.get("Geometry", {})
            element = LayoutElement(
                element_type=block_type,
                text=block.get("Text", ""),
                confidence=block.get("Confidence", 0.0),
                bounding_box=geometry.get("BoundingBox", {}),
                page=block.get("Page", 0),
                relationships=block.get("Relationships", []),
            )
            elements.append(element)

    return elements


def _extract_relationship_text(all_blocks: List[dict], relationships: List[dict]) -> str:
    """
    Extract text from related child blocks referenced in Textract relationships.

    Args:
        all_blocks: Full list of Textract blocks
        relationships: Textract relationship objects

    Returns:
        Concatenated text from related blocks
    """
    texts = []
    block_ids = {}
    for b in all_blocks:
        block_ids[b.get("Id")] = b

    for rel in relationships:
        if rel.get("Type") == "CHILD":
            for child_id in rel.get("Ids", []):
                child = block_ids.get(child_id, {})
                if child.get("Text"):
                    texts.append(child["Text"])

    return " ".join(texts)


def filter_layout_by_type(response: LayoutResponse, element_type: str) -> List[LayoutElement]:
    """
    Filter layout elements by type.

    Args:
        response: LayoutResponse from extract_layout_from_image
        element_type: Textract layout block type to filter

    Returns:
        Filtered list of LayoutElement objects
    """
    return [el for el in response.elements if el.element_type == element_type]


def get_layout_summary(response: LayoutResponse) -> dict:
    """
    Get a summary count of layout element types.

    Args:
        response: LayoutResponse from extract_layout_from_image

    Returns:
        Dictionary mapping element types to counts
    """
    summary = {}
    for el in response.elements:
        summary[el.element_type] = summary.get(el.element_type, 0) + 1
    return summary


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_layout.py <image_path>")
        sys.exit(1)

    img_path = sys.argv[1]
    result = extract_layout_from_image(img_path)
    summary = get_layout_summary(result)

    print(f"Layout extraction complete: {result.page_count} page(s), {len(result.elements)} elements")
    for elem_type, count in sorted(summary.items()):
        print(f"  {elem_type}: {count}")
