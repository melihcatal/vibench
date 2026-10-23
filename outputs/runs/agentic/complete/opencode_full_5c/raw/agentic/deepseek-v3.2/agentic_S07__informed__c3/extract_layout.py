import os
from typing import List, Dict, Any, Optional
from document_client import DocumentClient
from document_models import normalize_textract_response, TextBlock, BlockType


def extract_layout(
    image_path: str, region: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Extract blocks, lines, tables, or layout elements from a document using Amazon Textract.

    Args:
        image_path: Path to the image file
        region: AWS region (defaults to AWS_DEFAULT_REGION env var)

    Returns:
        List of layout elements with text, type, and geometry
    """
    # Read image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Initialize Textract client
    client = DocumentClient(region_name=region)

    # Call Textract API with layout analysis
    response = client.analyze_document(
        image_bytes, feature_types=["TABLES", "FORMS", "LAYOUT"]
    )

    # Normalize response
    result = normalize_textract_response(response)

    # Convert to simple dict format
    layout_elements = []

    # Add text blocks
    for block in result.text_blocks:
        layout_elements.append(
            {
                "type": block.block_type.value,
                "text": block.text,
                "confidence": block.confidence,
                "geometry": block.geometry,
                "id": block.id,
            }
        )

    # Add tables
    for table in result.tables:
        layout_elements.append(
            {
                "type": "TABLE",
                "row_count": table.row_count,
                "column_count": table.column_count,
                "geometry": table.geometry,
                "cell_count": len(table.cells),
            }
        )

    # Add key-value pairs
    for kv in result.key_value_pairs:
        layout_elements.append(
            {
                "type": "KEY_VALUE",
                "key": kv.key,
                "value": kv.value,
                "key_confidence": kv.key_confidence,
                "value_confidence": kv.value_confidence,
            }
        )

    return layout_elements
