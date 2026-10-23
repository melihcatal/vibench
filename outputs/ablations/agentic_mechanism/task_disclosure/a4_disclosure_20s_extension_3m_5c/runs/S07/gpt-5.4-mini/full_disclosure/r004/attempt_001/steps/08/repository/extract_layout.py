import os
from typing import Any, Dict, Optional

import requests


def extract_layout(document_bytes: bytes, mime_type: str = "application/pdf", model: Optional[str] = None, api_key: Optional[str] = None, base_url: Optional[str] = None) -> Dict[str, Any]:
    api_key = api_key or os.getenv("GOOGLE_CLOUD_VISION_API_KEY") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not api_key:
        raise ValueError("Missing Google Cloud Vision credentials")
    base_url = base_url or "https://vision.googleapis.com/v1/images:annotate"
    model = model or "document-text-detection"
    payload = {
        "requests": [
            {
                "image": {"content": document_bytes.decode("latin1")},
                "features": [{"type": model}],
                "imageContext": {"mimeType": mime_type},
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        headers["Authorization"] = f"Bearer {api_key}"
        response = requests.post(base_url, json=payload, headers=headers, timeout=60)
    else:
        response = requests.post(f"{base_url}?key={api_key}", json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    return response.json()
