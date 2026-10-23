import os
from typing import List, Dict, Any
import requests
from document_client import get_amazon_textract_client
from document_models import (
    LayoutExtractionRequest,
    LayoutExtractionResponse,
    LayoutBlock,
)


def extract_layout(image_path: str) -> LayoutExtractionResponse:
    """
    Extract blocks, lines, tables, or layout elements from a document using Amazon Textract.
    """
    client = get_amazon_textract_client()

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["LAYOUT"]
    )

    blocks = []
    for block in response.get("Blocks", []):
        if block["BlockType"] in ["LINE", "WORD", "TABLE", "CELL", "KEY_VALUE_SET"]:
            geometry = block.get("Geometry", {})
            bounding_box = geometry.get("BoundingBox", {})

            layout_block = LayoutBlock(
                block_type=block["BlockType"],
                text=block.get("Text", ""),
                confidence=block.get("Confidence", 0.0),
                bounding_box={
                    "left": bounding_box.get("Left", 0.0),
                    "top": bounding_box.get("Top", 0.0),
                    "width": bounding_box.get("Width", 0.0),
                    "height": bounding_box.get("Height", 0.0),
                },
                relationships=block.get("Relationships", []),
                page=block.get("Page", 1),
            )
            blocks.append(layout_block)

    return LayoutExtractionResponse(
        blocks=blocks, provider="amazon_textract", raw_response=response
    )
