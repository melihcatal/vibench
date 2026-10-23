import os
import sys
from pathlib import Path

import requests


GOOGLE_VISION_URL = "https://vision.googleapis.com/v1/images:annotate"


def extract_text(image_path: str) -> str:
    api_key = os.environ.get("GOOGLE_VISION_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_VISION_API_KEY is required")

    data = Path(image_path).read_bytes()
    payload = {
        "requests": [
            {
                "image": {"content": data.hex()},
                "features": [{"type": "TEXT_DETECTION"}],
            }
        ]
    }
    response = requests.post(
        GOOGLE_VISION_URL,
        params={"key": api_key},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    result = response.json()
    annotations = result.get("responses", [{}])[0]
    if "error" in annotations:
        raise RuntimeError(annotations["error"].get("message", "Google Vision API error"))
    texts = annotations.get("textAnnotations", [])
    return texts[0].get("description", "") if texts else ""


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: extract_text.py IMAGE_PATH")
    print(extract_text(sys.argv[1]))


if __name__ == "__main__":
    main()
