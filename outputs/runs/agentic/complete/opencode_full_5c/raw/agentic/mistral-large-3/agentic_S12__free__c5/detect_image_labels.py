import io
from typing import List
from vision_client import get_vision_client
from vision_models import ImageLabel, normalize_labels


def detect_image_labels(image_path: str) -> List[ImageLabel]:
    """Detects labels or objects in a static image using Google Cloud Vision API."""
    client = get_vision_client()

    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    image = {"content": content}
    response = client.label_detection(image=image)

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    return normalize_labels(
        [
            {
                "description": label.description,
                "score": label.score,
                "topicality": label.topicality,
            }
            for label in response.label_annotations
        ]
    )
