import os
from google.cloud import vision
from typing import List, Dict, Any


def detect_image_labels(image_path: str) -> List[Dict[str, Any]]:
    """
    Detects labels or objects in a static image using Google Cloud Vision API.

    Args:
        image_path: Path to the image file

    Returns:
        List of dictionaries containing label descriptions and confidence scores
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    results = []
    for label in labels:
        results.append(
            {
                "description": label.description,
                "score": label.score,
                "mid": label.mid,
                "topicality": label.topicality,
            }
        )

    return results
