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


def score_image_safety(image_path: str) -> List[Dict[str, Any]]:
    api_key = os.environ.get("GOOGLE_CLOUD_VISION_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GOOGLE_CLOUD_VISION_API_KEY or GOOGLE_API_KEY")

    payload = {
        "requests": [
            {
                "image": _load_image_content(image_path),
                "features": [{"type": "SAFE_SEARCH_DETECTION"}],
            }
        ]
    }
    response = requests.post(f"{API_URL}?key={api_key}", json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    safe_search = data["responses"][0].get("safeSearchAnnotation", {})
    return [
        {"category": key, "likelihood": value}
        for key, value in safe_search.items()
    ]


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: score_image_safety.py IMAGE_PATH")
    image_path = sys.argv[1]
    print(json.dumps(score_image_safety(image_path), indent=2))


if __name__ == "__main__":
    main()
