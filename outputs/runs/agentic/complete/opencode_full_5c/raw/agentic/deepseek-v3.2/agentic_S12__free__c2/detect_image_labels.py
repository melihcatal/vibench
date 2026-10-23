import os
from google.cloud import vision
from vision_client import get_vision_client


def detect_image_labels(image_path):
    """Detects labels or objects in a static image using Google Cloud Vision API."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    result = []
    for label in labels:
        result.append(
            {
                "description": label.description,
                "score": label.score,
                "topicality": label.topicality,
            }
        )

    return result
