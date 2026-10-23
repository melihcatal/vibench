import base64
import json
import os
import sys
from typing import Any, Dict, List

import requests


API_URL = "https://vision.googleapis.com/v1/images:annotate"


def _load_image_content(image_path: str) -> Dict[str, Any]:
    if image_path.startswith("http://") or image_path.startswith("https://"):
        return {"source": {"imageUri": image_path}}
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return {"content": encoded}


def detect_image_labels(image_path: str, max_results: int = 10) -> List[Dict[str, Any]]:
    api_key = os.environ.get("GOOGLE_CLOUD_VISION_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GOOGLE_CLOUD_VISION_API_KEY or GOOGLE_API_KEY")

    payload = {
        "requests": [
            {
                "image": _load_image_content(image_path),
                "features": [{"type": "LABEL_DETECTION", "maxResults": max_results}],
            }
        ]
    }
    response = requests.post(f"{API_URL}?key={api_key}", json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    annotations = data["responses"][0].get("labelAnnotations", [])
    return [
        {
            "description": item.get("description"),
            "score": item.get("score"),
            "mid": item.get("mid"),
        }
        for item in annotations
    ]


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: detect_image_labels.py IMAGE_PATH [MAX_RESULTS]")
    image_path = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    print(json.dumps(detect_image_labels(image_path, max_results=max_results), indent=2))


if __name__ == "__main__":
    main()
