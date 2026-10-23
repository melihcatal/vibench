import os
import sys
from pathlib import Path

import requests


def extract_text(image_path: str) -> str:
    api_key = os.environ.get("OCR_SPACE_API_KEY")
    if not api_key:
        raise RuntimeError("OCR_SPACE_API_KEY is required")

    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(image_path)

    with path.open("rb") as f:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"filename": (path.name, f)},
            data={"language": "eng", "isOverlayRequired": False},
            headers={"apikey": api_key},
            timeout=60,
        )
    response.raise_for_status()
    payload = response.json()

    if payload.get("IsErroredOnProcessing"):
        errors = payload.get("ErrorMessage") or payload.get("ErrorDetails") or "OCR failed"
        raise RuntimeError(errors)

    results = payload.get("ParsedResults") or []
    texts = []
    for item in results:
        text = item.get("ParsedText")
        if text:
            texts.append(text)
    return "\n".join(texts).strip()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python extract_text.py <image_path>")
    print(extract_text(sys.argv[1]))
