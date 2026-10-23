import os
from typing import Dict, Any, List
import requests
from document_client import get_document_client
from document_models import LayoutExtractionResponse, LayoutBlock


def extract_layout(image_path: str) -> LayoutExtractionResponse:
    """
    Extract layout elements (blocks, lines, paragraphs) from a document using Amazon Textract.
    """
    client = get_document_client("textract")
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    # Amazon Textract-specific request
    response = client.post(
        f"https://textract.{os.getenv('AWS_REGION')}.amazonaws.com",
        headers={
            "Content-Type": "application/x-amz-json-1.1",
            "X-Amz-Target": "Textract.DetectDocumentText"
        },
        data=content
    )
    
    response.raise_for_status()
    result = response.json()
    
    # Normalize response to local model
    blocks = []
    for block in result.get("Blocks", []):
        if block["BlockType"] in ["WORD", "LINE", "CELL", "TABLE"]:
            blocks.append(
                LayoutBlock(
                    block_type=block["BlockType"],
                    text=block.get("Text", ""),
                    bounding_box={
                        "left": block["Geometry"]["BoundingBox"]["Left"],
                        "top": block["Geometry"]["BoundingBox"]["Top"],
                        "width": block["Geometry"]["BoundingBox"]["Width"],
                        "height": block["Geometry"]["BoundingBox"]["Height"]
                    }
                )
            )
    
    return LayoutExtractionResponse(blocks=blocks, provider="amazon_textract")