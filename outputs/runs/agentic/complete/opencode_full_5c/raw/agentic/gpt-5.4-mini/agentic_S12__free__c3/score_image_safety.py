from vision_client import get_client
from vision_models import VisionRequest


def score_image_safety(image_path: str):
    client = get_client()
    return client.analyze(
        VisionRequest(image_path=image_path),
        "Check this image for unsafe or policy-sensitive visual content",
    )
