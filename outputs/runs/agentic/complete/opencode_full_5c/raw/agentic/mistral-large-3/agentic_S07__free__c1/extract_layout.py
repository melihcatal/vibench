from typing import Dict, List, Optional
import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from document_client import get_vision_client
from document_models import LayoutResponse, LayoutBlock


def extract_layout(image_path: str) -> LayoutResponse:
    """Extract layout elements (blocks, lines, tables) from a document using Google Cloud Vision."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    features = [{"type_": vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION}]

    request = types.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request)

    blocks = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            blocks.append(LayoutBlock.from_vision_block(block))

    return LayoutResponse(blocks=blocks)
