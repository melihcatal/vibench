from typing import Dict, List, Optional
import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from document_client import get_document_client
from document_models import LayoutResponse


def extract_layout(image_path: str) -> LayoutResponse:
    """Extract layout elements (blocks, paragraphs, lines) from a document using Google Cloud Vision."""
    client = get_document_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)
    feature = vision_v1.types.Feature(
        type_=vision_v1.types.Feature.Type.DOCUMENT_TEXT_DETECTION
    )

    request = vision_v1.types.AnnotateImageRequest(image=image, features=[feature])
    response = client.annotate_image(request)

    if not response.full_text_annotation.pages:
        return LayoutResponse(blocks=[], paragraphs=[], lines=[])

    page = response.full_text_annotation.pages[0]

    blocks = []
    for block in page.blocks:
        blocks.append(
            {
                "text": block.text,
                "bounding_box": {
                    "vertices": [
                        {"x": vertex.x, "y": vertex.y}
                        for vertex in block.bounding_box.vertices
                    ]
                },
                "block_type": vision_v1.Block.BlockType(block.block_type).name,
            }
        )

    paragraphs = []
    for paragraph in page.paragraphs:
        paragraphs.append(
            {
                "text": paragraph.text,
                "bounding_box": {
                    "vertices": [
                        {"x": vertex.x, "y": vertex.y}
                        for vertex in paragraph.bounding_box.vertices
                    ]
                },
            }
        )

    lines = []
    for line in page.lines:
        lines.append(
            {
                "text": line.text,
                "bounding_box": {
                    "vertices": [
                        {"x": vertex.x, "y": vertex.y}
                        for vertex in line.bounding_box.vertices
                    ]
                },
            }
        )

    return LayoutResponse(blocks=blocks, paragraphs=paragraphs, lines=lines)
