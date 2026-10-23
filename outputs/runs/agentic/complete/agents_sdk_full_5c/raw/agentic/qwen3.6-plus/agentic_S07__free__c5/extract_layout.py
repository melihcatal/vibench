"""
Extract layout elements from a document using AWS Textract AnalyzeDocument API.

Uses the LAYOUT feature of AWS Textract to identify and extract document
structure elements including sections, figures, tables, lists, headers,
footers, and text regions.
"""

import os
from typing import Optional, List

import boto3
from botocore.exceptions import ClientError

from document_client import (
    get_textract_client,
    prepare_textract_document,
    load_image_as_bytes,
    validate_image_size,
)
from document_models import (
    LayoutResult,
    LayoutElement,
    TextBlock,
    normalize_textract_layout_elements,
    normalize_textract_blocks,
)


# AWS Textract service and feature identifiers
TEXTRACT_SERVICE_NAME = "textract"
TEXTRACT_ANALYZE_DOCUMENT_API = "analyze_document"
TEXTRACT_LAYOUT_FEATURE = "LAYOUT"


def extract_layout_from_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> LayoutResult:
    """
    Extract layout elements from a document image using AWS Textract.
    
    This function uses the AWS Textract AnalyzeDocument API with the
    LAYOUT feature type to identify structural elements in the document
    such as sections, figures, tables, lists, headers, footers, and
    text regions.
    
    Args:
        image_path: Path to the image file (PNG, JPEG, TIFF).
        image_bytes: Raw image bytes (alternative to image_path).
        
    Returns:
        LayoutResult: Container with extracted layout elements and metadata.
        
    Raises:
        ValueError: If neither image_path nor image_bytes is provided.
        ClientError: If AWS Textract API call fails.
    """
    if image_bytes is None:
        if image_path is None:
            raise ValueError("Either image_path or image_bytes must be provided")
        image_bytes = load_image_as_bytes(image_path)
    
    if not validate_image_size(image_bytes):
        raise ValueError("Image exceeds 5MB limit for AWS Textract sync API")
    
    client = get_textract_client()
    document = prepare_textract_document(image_bytes)
    
    try:
        response = client.analyze_document(
            Document=document,
            FeatureTypes=[TEXTRACT_LAYOUT_FEATURE],
        )
    except ClientError as e:
        raise ClientError(
            e.response["Error"],
            f"Textract.{TEXTRACT_ANALYZE_DOCUMENT_API}",
        ) from e
    
    raw_blocks = response.get("Blocks", [])
    layout_elements = normalize_textract_layout_elements(raw_blocks)
    
    sections = [
        elem.text for elem in layout_elements
        if elem.element_type in ("LAYOUT_SECTION_HEADER", "LAYOUT_TITLE")
    ]
    
    page_count = len([b for b in raw_blocks if b.get("BlockType") == "PAGE"])
    
    return LayoutResult(
        elements=layout_elements,
        pages=max(page_count, 1),
        sections=sections,
    )


def extract_layout_from_bytes(image_bytes: bytes) -> List[LayoutElement]:
    """
    Convenience function to extract layout elements from image bytes.
    
    Args:
        image_bytes: Raw image bytes.
        
    Returns:
        List[LayoutElement]: Extracted layout elements.
    """
    result = extract_layout_from_image(image_bytes=image_bytes)
    return result.elements


def extract_layout_from_file(image_path: str) -> List[LayoutElement]:
    """
    Convenience function to extract layout elements from a file.
    
    Args:
        image_path: Path to the image file.
        
    Returns:
        List[LayoutElement]: Extracted layout elements.
    """
    result = extract_layout_from_image(image_path=image_path)
    return result.elements


def get_layout_summary(image_path: str) -> dict:
    """
    Get a summary of layout elements by type.
    
    Args:
        image_path: Path to the image file.
        
    Returns:
        dict: Mapping of element types to counts.
    """
    result = extract_layout_from_image(image_path=image_path)
    summary = {}
    for elem in result.elements:
        summary[elem.element_type] = summary.get(elem.element_type, 0) + 1
    return summary


def extract_sections_only(image_path: str) -> List[str]:
    """
    Extract only section headers and titles from the document.
    
    Args:
        image_path: Path to the image file.
        
    Returns:
        List[str]: List of section header texts.
    """
    result = extract_layout_from_image(image_path=image_path)
    return result.sections


def extract_elements_by_type(image_path: str, element_type: str) -> List[LayoutElement]:
    """
    Extract layout elements of a specific type.
    
    Args:
        image_path: Path to the image file.
        element_type: Type of elements to extract (e.g., LAYOUT_FIGURE, LAYOUT_TABLE).
        
    Returns:
        List[LayoutElement]: Filtered layout elements.
    """
    result = extract_layout_from_image(image_path=image_path)
    return [elem for elem in result.elements if elem.element_type == element_type]
