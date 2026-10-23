import os
from functools import lru_cache

from google.cloud import vision


@lru_cache(maxsize=1)
def get_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def get_project_language(default: str = "en") -> str:
    return os.getenv("VISION_LANGUAGE", default)
