import base64
import os
from typing import Optional

import requests


GOOGLE_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"


def extract_text(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> str:
    if image_bytes is None:
        if not image_path:
            raise ValueError("image_path or image_bytes is required")
        with open(image_path, "rb") as f:
            image_bytes = f.read()

    api_key = os.environ.get("GOOGLE_VISION_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_VISION_API_KEY is required")

    payload = {
        "requests": [
            {
                "image": {"content": base64.b64encode(image_bytes).decode("utf-8")},
                "features": [{"type": "TEXT_DETECTION"}],
            }
        ]
    }

    response = requests.post(
        f"{GOOGLE_VISION_API_URL}?key={api_key}",
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    responses = data.get("responses", [])
    if not responses:
        return ""

    text = responses[0].get("fullTextAnnotation", {}).get("text")
    if text:
        return text

    annotations = responses[0].get("textAnnotations", [])
    if annotations:
        return annotations[0].get("description", "")

    return ""
