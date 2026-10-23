from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageText
from typing import List


def detect_image_text(image_uri: str) -> List[ImageText]:
    """Detects text in an image using Google Cloud Vision API."""
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    detected_texts = []
    if texts:
        for text in texts:
            vertices = [
                {"x": vertex.x, "y": vertex.y} for vertex in text.bounding_poly.vertices
            ]
            detected_texts.append(
                ImageText(description=text.description, bounding_poly=vertices)
            )

    return detected_texts
