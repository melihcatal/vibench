# [SAME-SCENARIO] extract_layout.py

import os
from typing import List, Dict
from google.cloud import vision_v1
from .document_client import VisionClient
from .document_models import LayoutExtractionResponse

def extract_layout(image_bytes: bytes) -> LayoutExtractionResponse:
    """Extract layout elements (blocks, paragraphs, lines, words) from a document image using Google Cloud Vision Layout API.

    Args:
        image_bytes: raw image data.
    
    Returns:
        A LayoutExtractionResponse containing detected layout entities.
    """
    client = VisionClient()
    image = vision_v1.types.Image(content=image_bytes)
    response = client.service.document_text_detection(image=image)
    layout_entities = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            block_type = block.block_type.name.lower()
            layout_entities.append({"type": block_type, "bounding_box": str(block.bounding_box)})
    return LayoutExtractionResponse(layout_entities=layout_entities)
