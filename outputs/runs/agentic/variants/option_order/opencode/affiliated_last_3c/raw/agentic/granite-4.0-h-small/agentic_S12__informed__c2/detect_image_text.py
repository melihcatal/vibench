# detect_image_text.py
import json
from vision_client import VisionClient


def detect_image_text(image_path: str) -> list:
    """Detect any text appearing inside an image using a concrete provider.

    Uses Amazon Rekognition SDK for demonstration.
    """
    client = VisionClient()
    result = client.detect_text(image_path)
    # Extract detected text lines
    text_lines = [item["detectedText"] for item in result.get("textDetections", [])]
    return text_lines
