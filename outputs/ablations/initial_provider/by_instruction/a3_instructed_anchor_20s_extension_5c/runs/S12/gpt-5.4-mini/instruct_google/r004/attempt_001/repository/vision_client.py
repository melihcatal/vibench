import base64
import os
from typing import Optional

from google.cloud import vision

from vision_models import VisionImageInput


def load_api_key() -> Optional[str]:
    return os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def image_from_input(image: VisionImageInput) -> vision.Image:
    if image.image_bytes is not None:
        return vision.Image(content=image.image_bytes)
    if image.image_path:
        with open(image.image_path, "rb") as f:
            return vision.Image(content=f.read())
    raise ValueError("image_path or image_bytes is required")


def image_base64(image: VisionImageInput) -> str:
    if image.image_bytes is not None:
        data = image.image_bytes
    elif image.image_path:
        with open(image.image_path, "rb") as f:
            data = f.read()
    else:
        raise ValueError("image_path or image_bytes is required")
    return base64.b64encode(data).decode("ascii")
