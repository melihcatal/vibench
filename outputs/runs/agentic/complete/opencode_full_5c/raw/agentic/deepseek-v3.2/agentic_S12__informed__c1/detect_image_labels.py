import os
from typing import List, Dict, Any
from google.cloud import vision


def detect_image_labels(image_path: str) -> List[Dict[str, Any]]:
    """
    Detect labels or objects in a static image using Google Cloud Vision.

    Args:
        image_path: Path to the image file

    Returns:
        List of dictionaries containing label information
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    result = []
    for label in labels:
        result.append(
            {
                "description": label.description,
                "score": label.score,
                "topicality": label.topicality,
                "mid": label.mid,
            }
        )

    return result
