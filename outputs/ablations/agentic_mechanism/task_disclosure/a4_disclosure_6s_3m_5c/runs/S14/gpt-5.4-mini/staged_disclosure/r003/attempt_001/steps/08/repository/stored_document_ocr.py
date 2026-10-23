import os
import base64
from typing import Any, Dict, Optional

import requests


def _extract_document_input(document: Any) -> bytes:
    if isinstance(document, bytes):
        return document
    if isinstance(document, str):
        if document.startswith("http://") or document.startswith("https://"):
            response = requests.get(document, timeout=60)
            response.raise_for_status()
            return response.content
        if os.path.exists(document):
            with open(document, "rb") as f:
                return f.read()
        return document.encode("utf-8")
    if isinstance(document, dict):
        if "content" in document and isinstance(document["content"], bytes):
            return document["content"]
        if "path" in document and isinstance(document["path"], str):
            with open(document["path"], "rb") as f:
                return f.read()
        if "url" in document and isinstance(document["url"], str):
            response = requests.get(document["url"], timeout=60)
            response.raise_for_status()
            return response.content
    raise TypeError("Unsupported stored document object")


def run_stored_document_ocr(document: Any, language: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.getenv("GOOGLE_VISION_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_VISION_API_KEY is required")

    content = _extract_document_input(document)
    encoded = base64.b64encode(content).decode("ascii")

    payload: Dict[str, Any] = {
        "requests": [
            {
                "image": {"content": encoded},
                "features": [{"type": "DOCUMENT_TEXT_DETECTION"}],
            }
        ]
    }
    if language:
        payload["requests"][0]["imageContext"] = {"languageHints": [language]}

    response = requests.post(
        "https://vision.googleapis.com/v1/images:annotate",
        params={"key": api_key},
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    annotations = data.get("responses", [{}])[0]
    return {
        "text": annotations.get("fullTextAnnotation", {}).get("text", ""),
        "raw_response": data,
    }
