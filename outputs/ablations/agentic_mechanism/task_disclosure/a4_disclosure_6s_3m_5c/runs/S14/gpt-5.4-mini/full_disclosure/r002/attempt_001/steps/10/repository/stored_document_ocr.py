import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class OCRResult:
    text: str
    raw: Dict[str, Any]


def _require_env(name: str, fallback: Optional[str] = None) -> str:
    value = os.getenv(name, fallback)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def run_stored_document_ocr(bucket: str, object_key: str, *, storage_provider_url: Optional[str] = None, api_key: Optional[str] = None, model: str = "google/gemini-2.0-flash") -> OCRResult:
    base_url = (storage_provider_url or _require_env("STORAGE_PROVIDER_URL")).rstrip("/")
    token = api_key or _require_env("STORAGE_API_KEY")
    url = f"{base_url}/v1/documents/ocr"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "bucket": bucket,
        "object_key": object_key,
        "model": model,
    }
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    text = data.get("text") or data.get("ocr_text") or ""
    return OCRResult(text=text, raw=data)


def run_stored_document_ocr_from_bytes(content: bytes, *, filename: str, mime_type: str = "application/pdf", api_key: Optional[str] = None, ocr_api_url: Optional[str] = None, model: str = "google/gemini-2.0-flash") -> OCRResult:
    url = (ocr_api_url or _require_env("GOOGLE_CLOUD_VISION_API_URL", "https://vision.googleapis.com/v1/images:annotate")).rstrip("/")
    token = api_key or _require_env("GOOGLE_CLOUD_API_KEY")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    encoded = base64.b64encode(content).decode("ascii")
    payload = {
        "requests": [
            {
                "image": {"content": encoded},
                "features": [{"type": "DOCUMENT_TEXT_DETECTION"}],
                "imageContext": {"languageHints": ["en"]},
                "inputConfig": {"mimeType": mime_type, "filename": filename, "model": model},
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    responses = data.get("responses", [])
    text = ""
    if responses:
        text = responses[0].get("fullTextAnnotation", {}).get("text", "")
    return OCRResult(text=text, raw=data)
