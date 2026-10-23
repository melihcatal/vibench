import base64
import os
from typing import Any, Dict, Optional

from google.cloud import vision
from google.cloud import documentai_v1 as documentai


def _load_image_content(image_uri: Optional[str], image_bytes: Optional[bytes]) -> bytes:
    if image_bytes:
        return image_bytes
    if image_uri and os.path.exists(image_uri):
        with open(image_uri, "rb") as f:
            return f.read()
    if image_uri and image_uri.startswith("gs://"):
        return image_uri.encode("utf-8")
    raise ValueError("image_uri or image_bytes is required")


def vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def documentai_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def vision_image_from_request(image_uri: Optional[str] = None, image_bytes: Optional[bytes] = None) -> vision.Image:
    content = _load_image_content(image_uri, image_bytes)
    if image_uri and image_uri.startswith("gs://"):
        return vision.Image(source=vision.ImageSource(image_uri=image_uri))
    return vision.Image(content=content)


def documentai_raw_document(image_uri: Optional[str], image_bytes: Optional[bytes]) -> documentai.RawDocument:
    content = _load_image_content(image_uri, image_bytes)
    mime_type = "image/png"
    if image_uri:
        lower = image_uri.lower()
        if lower.endswith(".jpg") or lower.endswith(".jpeg"):
            mime_type = "image/jpeg"
        elif lower.endswith(".tif") or lower.endswith(".tiff"):
            mime_type = "image/tiff"
    return documentai.RawDocument(content=content, mime_type=mime_type)


def processor_name(project_id: str, location: str, processor_id: str) -> str:
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(name, default)
