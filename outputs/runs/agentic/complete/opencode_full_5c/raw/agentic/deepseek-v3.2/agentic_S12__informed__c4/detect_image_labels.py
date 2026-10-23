import os
from typing import List, Dict, Any
from vision_client import get_vision_client


def detect_image_labels(image_path: str, max_labels: int = 10) -> List[Dict[str, Any]]:
    """
    Detect labels or objects in a static image using Amazon Rekognition.

    Args:
        image_path: Path to the image file
        max_labels: Maximum number of labels to return

    Returns:
        List of label dictionaries with 'name' and 'confidence' keys
    """
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.detect_labels(Image={"Bytes": image_bytes}, MaxLabels=max_labels)

    labels = []
    for label in response["Labels"]:
        labels.append({"name": label["Name"], "confidence": label["Confidence"]})

    return labels
