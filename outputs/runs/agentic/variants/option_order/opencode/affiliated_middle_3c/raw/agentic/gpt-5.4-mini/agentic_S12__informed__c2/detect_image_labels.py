from google.cloud import vision

from vision_client import get_vision_client, load_image_bytes
from vision_models import VisionRequest, normalize_labels


def detect_image_labels(image_path: str):
    req = VisionRequest(image_path=image_path)
    client = get_vision_client()
    image = vision.Image(content=load_image_bytes(req.image_path))
    response = client.label_detection(image=image)
    return normalize_labels(
        [
            {"name": label.description, "score": label.score}
            for label in response.label_annotations
        ]
    )
