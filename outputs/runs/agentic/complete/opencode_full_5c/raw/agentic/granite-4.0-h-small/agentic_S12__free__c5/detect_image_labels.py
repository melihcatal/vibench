# SAME-SCENARIO
# Detect labels or objects in a static image using AWS Rekognition
import json
from vision_client import VisionClient


def detect_image_labels(image_path: str) -> list:
    """Detect objects/labels in a static image and return a list of detected labels.

    Args:
        image_path: Local path to the image file.

    Returns:
        A list of dictionaries with label details.
    """
    client = VisionClient("aws")  # Provider identifier in code
    response = client.detect_labels(image_path)
    # Normalize response to a common format
    normalized = []
    for label in response.get("Labels", []):
        normalized.append(
            {
                "Name": label.get("Name"),
                "Confidence": label.get("Confidence"),
            }
        )
    return normalized
