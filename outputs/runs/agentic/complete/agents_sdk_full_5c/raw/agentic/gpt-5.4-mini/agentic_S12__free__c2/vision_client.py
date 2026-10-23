import os
from typing import Optional

from google.cloud import vision

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
VISION_API_HOST = os.getenv("GOOGLE_CLOUD_VISION_API_HOST", "vision.googleapis.com")


def get_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient(client_options={"api_endpoint": VISION_API_HOST})


def get_image_source(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> bytes:
    if image_bytes is not None:
        return image_bytes
    if image_path:
        with open(image_path, "rb") as f:
            return f.read()
    raise ValueError("image_path or image_bytes is required")
