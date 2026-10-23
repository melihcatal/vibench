from __future__ import annotations

import mimetypes
import os
from pathlib import Path
from typing import Optional

from google.cloud import vision

from vision_models import ImageSource


VISION_PROVIDER = "google-cloud-vision"


def get_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def load_image_bytes(image_path: str) -> bytes:
    return Path(image_path).read_bytes()


def detect_mime_type(image_path: str) -> Optional[str]:
    mime_type, _ = mimetypes.guess_type(image_path)
    return mime_type


def build_image_source(image_path: str) -> ImageSource:
    return ImageSource(image_path=image_path, mime_type=detect_mime_type(image_path))


def google_credentials_path() -> Optional[str]:
    return os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def build_vision_image(image_path: str) -> vision.Image:
    return vision.Image(content=load_image_bytes(image_path))
