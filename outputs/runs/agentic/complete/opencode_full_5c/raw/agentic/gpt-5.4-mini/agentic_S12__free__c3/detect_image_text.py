from vision_client import get_client
from vision_models import VisionRequest


def detect_image_text(image_path: str):
    client = get_client()
    return client.analyze(
        VisionRequest(image_path=image_path), "Detect all visible text in this image"
    )
