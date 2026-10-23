from google.cloud import vision

from vision_client import get_vision_client, load_image_bytes
from vision_models import normalize_text_blocks


def detect_image_text(image_path: str):
    client = get_vision_client()
    image = vision.Image(content=load_image_bytes(image_path))
    response = client.text_detection(image=image)
    return normalize_text_blocks(
        [
            {"text": ann.description, "confidence": getattr(ann, "confidence", 0.0)}
            for ann in response.text_annotations[1:]
        ]
    )
