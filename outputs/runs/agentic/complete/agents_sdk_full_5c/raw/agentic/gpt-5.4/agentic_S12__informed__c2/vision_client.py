from __future__ import annotations

import base64
import os
from typing import Optional

from google.cloud import vision

from vision_models import ImageSource

GOOGLE_VISION_PROVIDER = "google-cloud-vision"
GOOGLE_VISION_MODEL = "builtin/latest"


class VisionClientFactory:
    @staticmethod
    def create_image_annotator_client() -> vision.ImageAnnotatorClient:
        return vision.ImageAnnotatorClient()


def load_image_bytes(source: ImageSource) -> bytes:
    if source.content_bytes is not None:
        return source.content_bytes
    if source.path:
        with open(source.path, "rb") as infile:
            return infile.read()
    raise ValueError("ImageSource requires content_bytes or path for Google Cloud Vision requests.")


def build_vision_image(source: ImageSource) -> vision.Image:
    if source.uri:
        return vision.Image(source=vision.ImageSource(image_uri=source.uri))
    return vision.Image(content=load_image_bytes(source))


def image_source_from_path(path: str) -> ImageSource:
    return ImageSource(path=path)


def image_source_from_uri(uri: str) -> ImageSource:
    return ImageSource(uri=uri)


def image_source_from_base64(data: str) -> ImageSource:
    return ImageSource(content_bytes=base64.b64decode(data))


def google_credentials_path() -> Optional[str]:
    return os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
