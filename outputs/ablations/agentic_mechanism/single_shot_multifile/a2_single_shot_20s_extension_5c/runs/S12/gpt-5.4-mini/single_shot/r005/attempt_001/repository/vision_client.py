import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from google.cloud import vision


def load_vision_config() -> dict:
    return {
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
        "credentials": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        "vision_endpoint": os.getenv("GOOGLE_CLOUD_VISION_ENDPOINT", "vision.googleapis.com"),
    }


def vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def resolve_input_path(image_path: str) -> str:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(image_path)
    return str(path)


@contextmanager
def open_image_bytes(image_path: str) -> Iterator[bytes]:
    with open(image_path, "rb") as fh:
        yield fh.read()
