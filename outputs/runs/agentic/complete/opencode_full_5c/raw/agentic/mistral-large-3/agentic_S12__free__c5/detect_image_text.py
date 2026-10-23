import io
from typing import List
from vision_client import get_vision_client
from vision_models import ImageTextDetection, normalize_text_detections


def detect_image_text(image_path: str) -> List[ImageTextDetection]:
    """Detects text in an image using Google Cloud Vision API."""
    client = get_vision_client()

    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    image = {"content": content}
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    return normalize_text_detections(
        [
            {
                "description": text.description,
                "bounding_box": {
                    "vertices": [
                        {"x": vertex.x, "y": vertex.y}
                        for vertex in text.bounding_box.vertices
                    ]
                },
            }
            for text in response.text_annotations[:10]
        ]
    )
