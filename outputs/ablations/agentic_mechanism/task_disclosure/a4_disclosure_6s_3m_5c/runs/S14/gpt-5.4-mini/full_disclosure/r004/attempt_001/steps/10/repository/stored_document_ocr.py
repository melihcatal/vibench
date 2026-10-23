import base64
import json
import os
from typing import Any, Dict, Optional

import requests


GOOGLE_CLOUD_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"


def _load_bytes(source: Any) -> bytes:
    if source is None:
        raise ValueError("source is required")
    if isinstance(source, bytes):
        return source
    if isinstance(source, bytearray):
        return bytes(source)
    if isinstance(source, str):
        if source.startswith("http://") or source.startswith("https://"):
            response = requests.get(source, timeout=60)
            response.raise_for_status()
            return response.content
        with open(source, "rb") as f:
            return f.read()
    if hasattr(source, "read"):
        data = source.read()
        if isinstance(data, str):
            data = data.encode("utf-8")
        return data
    raise TypeError("unsupported source type")


def run_ocr_on_stored_document(
    source: Any,
    api_key: Optional[str] = None,
    language_hints: Optional[list[str]] = None,
) -> Dict[str, Any]:
    api_key = api_key or os.getenv("GOOGLE_CLOUD_VISION_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_CLOUD_VISION_API_KEY or GOOGLE_API_KEY is required")
    image_bytes = _load_bytes(source)
    payload: Dict[str, Any] = {
        "requests": [
            {
                "image": {"content": base64.b64encode(image_bytes).decode("ascii")},
                "features": [{"type": "TEXT_DETECTION"}],
            }
        ]
    }
    if language_hints:
        payload["requests"][0]["imageContext"] = {"languageHints": language_hints}
    response = requests.post(
        GOOGLE_CLOUD_VISION_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    annotations = data.get("responses", [{}])[0]
    if "error" in annotations:
        raise RuntimeError(json.dumps(annotations["error"]))
    text = annotations.get("fullTextAnnotation", {}).get("text", "")
    return {"text": text, "raw": data}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("--api-key")
    parser.add_argument("--language-hints", nargs="*")
    args = parser.parse_args()
    result = run_ocr_on_stored_document(args.source, api_key=args.api_key, language_hints=args.language_hints)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
