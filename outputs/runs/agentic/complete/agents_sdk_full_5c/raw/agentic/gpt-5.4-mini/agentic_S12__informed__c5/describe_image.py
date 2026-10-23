from __future__ import annotations

from vision_client import VisionClient
from vision_models import ImageRequest


def describe_image(image_path: str):
    client = VisionClient()
    return client.describe_image(ImageRequest(image_path=image_path, detail="short"))
