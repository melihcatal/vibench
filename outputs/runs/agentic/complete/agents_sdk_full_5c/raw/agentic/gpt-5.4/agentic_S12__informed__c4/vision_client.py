from __future__ import annotations

import base64
import mimetypes
import os
from typing import Any, Dict, Optional, Tuple

from google.cloud import vision


DEFAULT_MODEL = "google-cloud-vision"
DEFAULT_PROVIDER = "Google Cloud Vision"


def load_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def infer_mime_type(path: str) -> str:
    mime_type, _ = mimetypes.guess_type(path)
    return mime_type or "application/octet-stream"


def load_image_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def build_image_source(path: Optional[str] = None, uri: Optional[str] = None) -> Tuple[vision.Image, Dict[str, Any]]:
    if not path and not uri:
        raise ValueError("Either path or uri must be provided.")
    if path:
        content = load_image_bytes(path)
        image = vision.Image(content=content)
        return image, {
            "path": path,
            "uri": None,
            "mime_type": infer_mime_type(path),
            "bytes_b64": base64.b64encode(content).decode("ascii"),
        }
    image = vision.Image(source=vision.ImageSource(image_uri=uri))
    return image, {
        "path": None,
        "uri": uri,
        "mime_type": None,
    }


def ensure_env_ready() -> Dict[str, Optional[str]]:
    return {
        "provider": DEFAULT_PROVIDER,
        "model": DEFAULT_MODEL,
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    }
