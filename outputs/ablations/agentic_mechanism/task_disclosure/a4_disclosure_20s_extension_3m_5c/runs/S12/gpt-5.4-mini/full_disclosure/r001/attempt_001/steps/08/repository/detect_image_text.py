import base64
import json
import os
from typing import Any, Dict, Optional

import requests


GOOGLE_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"


def _load_image_content(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> str:
    if image_bytes is not None:
        return base64.b64encode(image_bytes).decode("utf-8")
    if image_path is None:
        raise ValueError("image_path or image_bytes is required")
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def detect_image_text(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None, language_hints: Optional[list[str]] = None) -> Dict[str, Any]:
    api_key = os.environ.get("GOOGLE_VISION_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_VISION_API_KEY is required")

    payload: Dict[str, Any] = {
        "requests": [
            {
                "image": {"content": _load_image_content(image_path=image_path, image_bytes=image_bytes)},
                "features": [{"type": "TEXT_DETECTION"}],
            }
        ]
    }
    if language_hints:
        payload["requests"][0]["imageContext"] = {"languageHints": language_hints}

    response = requests.post(
        GOOGLE_VISION_API_URL,
        params={"key": api_key},
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    annotations = data.get("responses", [{}])[0].get("textAnnotations", [])
    full_text = annotations[0]["description"] if annotations else ""
    return {"text": full_text, "annotations": annotations, "raw": data}
