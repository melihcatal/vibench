import os

from vision_client import VisionClient
from vision_models import normalize_text_detection

def detect_image_text(image_path: str) -> list[str]:
    """Detect and extract any text appearing in a static image using Amazon Rekognition.

    Returns a list of detected text strings.
    """
    client = VisionClient(service='rekognition')
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    response = client.detect_text(Image={'Bytes': image_bytes})
    raw_texts = response.get('TextDetections', [])
    return normalize_text_detection(raw_texts)
