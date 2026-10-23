import os
from typing import List, Dict, Any
from document_client import DocumentClient
from document_models import TextBlock, TextractResponseParser


def extract_layout_elements(image_bytes: bytes) -> Dict[str, Any]:
    """
    Extract layout elements (blocks, lines) from a document using Amazon Textract.

    Args:
        image_bytes: Bytes of the document image

    Returns:
        Dictionary containing layout elements
    """
    # Initialize Textract client
    client = DocumentClient()

    # Call Textract AnalyzeDocument API with LAYOUT feature
    response = client.analyze_document(
        document_bytes=image_bytes, feature_types=["LAYOUT"]
    )

    # Parse response
    text_blocks = TextractResponseParser.parse_text_blocks(response)

    # Extract layout information
    layout_elements = []
    for block in text_blocks:
        geometry = block.geometry
        bbox = geometry.get("BoundingBox", {})

        layout_elements.append(
            {
                "text": block.text,
                "confidence": block.confidence,
                "block_type": block.block_type,
                "bounding_box": {
                    "left": bbox.get("Left", 0),
                    "top": bbox.get("Top", 0),
                    "width": bbox.get("Width", 0),
                    "height": bbox.get("Height", 0),
                },
                "polygon": geometry.get("Polygon", []),
            }
        )

    return {
        "layout_elements": layout_elements,
        "total_elements": len(layout_elements),
        "provider": "Amazon Textract",
    }


def extract_document_structure(image_bytes: bytes) -> Dict[str, Any]:
    """
    Extract document structure including pages, blocks, and lines.

    Args:
        image_bytes: Bytes of the document image

    Returns:
        Structured document representation
    """
    client = DocumentClient()

    # Use both LAYOUT and FORMS features for comprehensive structure
    response = client.analyze_document(
        document_bytes=image_bytes, feature_types=["LAYOUT", "FORMS"]
    )

    # Parse blocks by type
    blocks_by_type = {}
    for block in response.get("Blocks", []):
        block_type = block.get("BlockType")
        if block_type not in blocks_by_type:
            blocks_by_type[block_type] = []

        block_data = {
            "id": block.get("Id"),
            "confidence": block.get("Confidence", 0.0),
            "geometry": block.get("Geometry", {}),
        }

        if block_type == "LINE":
            block_data["text"] = block.get("Text", "")

        blocks_by_type[block_type].append(block_data)

    return {
        "blocks_by_type": blocks_by_type,
        "total_blocks": len(response.get("Blocks", [])),
        "pages": response.get("DocumentMetadata", {}).get("Pages", 1),
        "provider": "Amazon Textract",
    }
