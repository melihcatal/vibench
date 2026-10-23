from __future__ import annotations

import base64
import json
import os
from typing import Any, Dict, Optional, Tuple
from urllib.request import Request, urlopen

from google.cloud import vision


GOOGLE_VISION_ENDPOINT = "https://vision.googleapis.com/v1/images:annotate"
GOOGLE_TRANSLATE_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"
GOOGLE_GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
GOOGLE_PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def load_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as fh:
        return fh.read()


def image_to_b64(image_path: str) -> str:
    return base64.b64encode(load_bytes(image_path)).decode("utf-8")


def build_vision_image(image_path: Optional[str] = None, image_uri: Optional[str] = None) -> vision.Image:
    if image_path:
        return vision.Image(content=load_bytes(image_path))
    if image_uri:
        return vision.Image(source=vision.ImageSource(image_uri=image_uri))
    raise ValueError("image_path or image_uri is required")


def get_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def post_json(url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, method="POST")
    request.add_header("Content-Type", "application/json")
    for key, value in (headers or {}).items():
        request.add_header(key, value)
    with urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def build_gemini_parts(prompt: str, image_path: str, mime_type: str = "image/jpeg") -> Dict[str, Any]:
    return {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_to_b64(image_path),
                        }
                    },
                ]
            }
        ]
    }


def parse_gemini_text(response: Dict[str, Any]) -> str:
    candidates = response.get("candidates", [])
    if not candidates:
        return ""
    parts = candidates[0].get("content", {}).get("parts", [])
    return " ".join(part.get("text", "").strip() for part in parts if part.get("text")).strip()


def split_gcs_uri(gcs_uri: str) -> Tuple[str, str]:
    if not gcs_uri.startswith("gs://"):
        raise ValueError("Expected Google Cloud Storage URI starting with gs://")
    path = gcs_uri[5:]
    bucket, _, blob = path.partition("/")
    return bucket, blob
