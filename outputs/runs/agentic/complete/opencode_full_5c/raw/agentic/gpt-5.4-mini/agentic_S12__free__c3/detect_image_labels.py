from vision_client import get_client
from vision_models import VisionRequest


def detect_image_labels(image_path: str):
    client = get_client()
    return client.analyze(
        VisionRequest(image_path=image_path), "Detect labels and objects in this image"
    )
