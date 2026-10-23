import os
from typing import Any, Dict

from google.cloud import vision


def vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def image_path_from_input(image_input: str) -> str:
    return image_input


def load_env() -> Dict[str, Any]:
    return {
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    }
