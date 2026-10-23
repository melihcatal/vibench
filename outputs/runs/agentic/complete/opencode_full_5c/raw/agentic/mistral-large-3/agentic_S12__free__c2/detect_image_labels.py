import os
from typing import List
from vision_client import AWSVisionClient
from vision_models import normalize_labels_response


def detect_image_labels(image_path: str) -> List[dict]:
    """Detect labels in an image using AWS Rekognition."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    client = AWSVisionClient()
    response = client.detect_labels(image_bytes)
    normalized_response = normalize_labels_response(response)

    return [
        {
            "label": label["Name"],
            "confidence": label["Confidence"],
            "parents": label["Parents"],
        }
        for label in normalized_response.Labels
    ]
