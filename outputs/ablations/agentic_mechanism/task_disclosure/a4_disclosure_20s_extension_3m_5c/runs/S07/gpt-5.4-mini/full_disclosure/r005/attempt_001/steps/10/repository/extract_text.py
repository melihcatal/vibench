import base64
import json
import os
import urllib.request
from typing import Optional


GOOGLE_VISION_ENDPOINT = "https://vision.googleapis.com/v1/images:annotate"


def extract_text(image_path: str, api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("GOOGLE_VISION_API_KEY")
    if not key:
        raise ValueError("GOOGLE_VISION_API_KEY is required")
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("ascii")
    payload = {
        "requests": [
            {
                "image": {"content": image_b64},
                "features": [{"type": "TEXT_DETECTION"}],
            }
        ]
    }
    data = json.dumps(payload).encode("utf-8")
    url = f"{GOOGLE_VISION_ENDPOINT}?key={key}"
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    responses = result.get("responses", [])
    if not responses:
        return ""
    annotation = responses[0]
    if "error" in annotation:
        message = annotation["error"].get("message", "Google Vision OCR error")
        raise RuntimeError(message)
    text = annotation.get("fullTextAnnotation", {}).get("text")
    if text:
        return text
    return annotation.get("textAnnotations", [{}])[0].get("description", "")
