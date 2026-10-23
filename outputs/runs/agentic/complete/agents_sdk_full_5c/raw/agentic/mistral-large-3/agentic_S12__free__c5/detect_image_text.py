import os
from typing import List
from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import TextDetectionResponse


def detect_text(image_path: str) -> TextDetectionResponse:
    """Detect text in a static image using Google Cloud Vision API."""
    client = get_vision_client()
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    image = vision_v1.Image(content=content)
    response = client.text_detection(image=image)
    
    return TextDetectionResponse(
        text=response.full_text_annotation.text if response.full_text_annotation else "",
        blocks=[
            {
                "text": block.text,
                "bounding_box": {
                    "vertices": [{"x": vertex.x, "y": vertex.y} for vertex in block.bounding_box.vertices]
                }
            }
            for block in response.full_text_annotation.pages[0].blocks
        ] if response.full_text_annotation else []
    )