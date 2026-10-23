from google.cloud import vision
from vision_client import get_vision_client
from vision_models import DetectedText
from typing import List


def detect_image_text(image_uri: str) -> List[DetectedText]:
    """Detects text in the image located at the given URI."""
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first text annotation is the full text block.
        full_text = texts[0].description
        return [DetectedText(text=full_text)]
    return []
