from typing import Dict, List, Optional
import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from document_client import get_google_vision_client
from document_models import LayoutResponse, LayoutBlock


def extract_layout(image_path: str) -> LayoutResponse:
    """Extract layout elements (blocks, paragraphs, lines) from a document using Google Cloud Vision."""
    client = get_google_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    features = [{"type": vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION}]

    request = types.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request)

    if not response.full_text_annotation:
        return LayoutResponse(provider="google_vision", blocks=[])

    blocks = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            block_text = block.text
            bounding_box = {
                "vertices": [
                    {"x": vertex.x, "y": vertex.y}
                    for vertex in block.bounding_box.vertices
                ]
            }

            paragraphs = []
            for paragraph in block.paragraphs:
                paragraph_text = paragraph.text
                paragraph_bbox = {
                    "vertices": [
                        {"x": vertex.x, "y": vertex.y}
                        for vertex in paragraph.bounding_box.vertices
                    ]
                }

                lines = []
                for line in paragraph.words:
                    line_text = "".join([symbol.text for symbol in line.symbols])
                    line_bbox = {
                        "vertices": [
                            {"x": vertex.x, "y": vertex.y}
                            for vertex in line.bounding_box.vertices
                        ]
                    }
                    lines.append({"text": line_text, "bounding_box": line_bbox})

                paragraphs.append(
                    {
                        "text": paragraph_text,
                        "bounding_box": paragraph_bbox,
                        "lines": lines,
                    }
                )

            blocks.append(
                LayoutBlock(
                    block_type="text",
                    text=block_text,
                    bounding_box=bounding_box,
                    paragraphs=paragraphs,
                )
            )

    return LayoutResponse(provider="google_vision", blocks=blocks)
