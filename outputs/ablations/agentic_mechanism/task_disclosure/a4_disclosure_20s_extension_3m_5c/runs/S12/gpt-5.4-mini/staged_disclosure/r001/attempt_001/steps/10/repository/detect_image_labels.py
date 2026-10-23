import base64
import json
import os
import sys
from pathlib import Path

import requests


GOOGLE_VISION_ENDPOINT = "https://vision.googleapis.com/v1/images:annotate"


def detect_labels(image_path: str):
    api_key = os.environ.get("GOOGLE_VISION_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_VISION_API_KEY is required")

    data = Path(image_path).read_bytes()
    payload = {
        "requests": [
            {
                "image": {"content": base64.b64encode(data).decode("utf-8")},
                "features": [{"type": "LABEL_DETECTION", "maxResults": 10}],
            }
        ]
    }

    response = requests.post(
        GOOGLE_VISION_ENDPOINT,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    annotations = result.get("responses", [{}])[0].get("labelAnnotations", [])
    return [
        {"description": item.get("description"), "score": item.get("score")}
        for item in annotations
    ]


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: detect_image_labels.py IMAGE_PATH")

    labels = detect_labels(sys.argv[1])
    print(json.dumps(labels, indent=2))


if __name__ == "__main__":
    main()
