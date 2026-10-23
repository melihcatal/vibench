import os
from typing import List
from vision_client import AWSVisionClient
from vision_models import normalize_text_detections, extract_text_detections


def detect_image_text(image_path: str) -> List[str]:
    """Detect text appearing inside an image using AWS Rekognition."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    client = AWSVisionClient()
    response = client.detect_text(image_bytes)
    normalized_response = normalize_text_detections(response)

    return extract_text_detections(normalized_response.TextDetections)
