from typing import Dict, List, Optional
import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from document_client import get_google_vision_client
from document_models import LayoutResponse


def extract_layout(image_path: str) -> LayoutResponse:
    """Extract layout elements (blocks, paragraphs, lines) from a document using Google Cloud Vision."""
    client = get_google_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    features = [{"type_": vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION}]

    request = types.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request)

    if not response.full_text_annotation:
        return LayoutResponse(blocks=[], paragraphs=[], lines=[])

    blocks = []
    paragraphs = []
    lines = []

    for page in response.full_text_annotation.pages:
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
                    "block_type": block.block_type.name,
                }
            )

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
