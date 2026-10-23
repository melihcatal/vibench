import base64
import json
import os
from typing import Any, Dict, Optional

import requests


GOOGLE_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"


def _load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def _request_payload(image_bytes: bytes) -> Dict[str, Any]:
    return {
        "requests": [
            {
                "image": {"content": base64.b64encode(image_bytes).decode("utf-8")},
                "features": [{"type": "TEXT_DETECTION", "maxResults": 10}],
            }
        ]
    }


def detect_image_text(image_path: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    api_key = api_key or os.environ.get("GOOGLE_VISION_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Missing Google Vision API key in GOOGLE_VISION_API_KEY or GOOGLE_API_KEY")

    image_bytes = _load_image_bytes(image_path)
    response = requests.post(
        GOOGLE_VISION_API_URL,
        params={"key": api_key},
        headers={"Content-Type": "application/json"},
        data=json.dumps(_request_payload(image_bytes)),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    annotations = data.get("responses", [{}])[0].get("textAnnotations", [])
    full_text = annotations[0].get("description", "") if annotations else ""
    words = [item.get("description", "") for item in annotations[1:]]

    return {
        "full_text": full_text,
        "words": words,
        "raw_response": data,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Detect text in an image using Google Cloud Vision API")
    parser.add_argument("image_path")
    parser.add_argument("--api-key", dest="api_key")
    args = parser.parse_args()

    result = detect_image_text(args.image_path, args.api_key)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
