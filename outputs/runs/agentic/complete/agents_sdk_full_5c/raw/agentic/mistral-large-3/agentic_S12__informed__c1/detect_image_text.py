from typing import List
import os
from google.cloud import vision
from vision_models import TextDetectionResponse


def detect_image_text(image_path: str) -> TextDetectionResponse:
    """Detect text in a static image using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    return TextDetectionResponse(
        text=texts[0].description if texts else "",
        bounding_boxes=[{
            "vertices": [{"x": vertex.x, "y": vertex.y} for vertex in text.bounding_poly.vertices]
        } for text in texts[1:]] if len(texts) > 1 else []
    )