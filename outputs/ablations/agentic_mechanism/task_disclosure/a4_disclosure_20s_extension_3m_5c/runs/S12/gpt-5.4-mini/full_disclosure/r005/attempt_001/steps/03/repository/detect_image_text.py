import base64
import json
import os
from typing import Any, Dict, List, Optional

import requests


GOOGLE_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"


def _load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def _to_data_url(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("ascii")


def detect_image_text(image_path: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.environ.get("GOOGLE_VISION_API_KEY")
    if not key:
        raise ValueError("GOOGLE_VISION_API_KEY is required")

    image_bytes = _load_image_bytes(image_path)
    payload = {
        "requests": [
            {
                "image": {"content": _to_data_url(image_bytes)},
                "features": [{"type": "TEXT_DETECTION", "maxResults": 10}],
            }
        ]
    }

    response = requests.post(
        f"{GOOGLE_VISION_API_URL}?key={key}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    annotations: List[Dict[str, Any]] = []
    text = ""

    responses = data.get("responses", [])
    if responses:
        annotation_response = responses[0]
        text = annotation_response.get("fullTextAnnotation", {}).get("text", "")
        for annotation in annotation_response.get("textAnnotations", []):
            annotations.append(
                {
                    "description": annotation.get("description", ""),
                    "boundingPoly": annotation.get("boundingPoly", {}),
                }
            )

    return {"text": text, "annotations": annotations, "raw": data}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Detect text in an image using Google Cloud Vision API")
    parser.add_argument("image_path")
    parser.add_argument("--api-key", dest="api_key")
    args = parser.parse_args()
    print(json.dumps(detect_image_text(args.image_path, args.api_key), ensure_ascii=False))
