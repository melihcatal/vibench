from vision_client import get_client
from vision_models import VisionRequest


def describe_image(image_path: str):
    client = get_client()
    return client.analyze(
        VisionRequest(image_path=image_path),
        "Generate a short visual description of this image",
    )
