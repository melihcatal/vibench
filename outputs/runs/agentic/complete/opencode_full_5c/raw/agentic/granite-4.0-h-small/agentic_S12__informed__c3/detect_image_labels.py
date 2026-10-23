import os
from vision_client import VisionClient


def detect_image_labels(image_path: str) -> list:
    """Detect labels/objects in a static image using Google Cloud Vision.

    Args:
        image_path: Path to the input image file.

    Returns:
        A list of detected label descriptions.
    """
    client = VisionClient(service="google-cloud-vision")
    response = client.detect_labels(image_path)
    # Extract label annotations from response
    labels = [
        annotation["description"] for annotation in response.get("labelAnnotations", [])
    ]
    return labels
