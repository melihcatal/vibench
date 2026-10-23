import base64
import json
import os
import sys
from typing import Any, Dict

import requests


GOOGLE_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"


def _load_document_payload(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("stored document object must be a JSON object")
    return data


def _build_request(document: Dict[str, Any]) -> Dict[str, Any]:
    if "content_base64" in document:
        content = document["content_base64"]
    elif "content_path" in document:
        with open(document["content_path"], "rb") as f:
            content = base64.b64encode(f.read()).decode("ascii")
    else:
        raise ValueError("document must include content_base64 or content_path")

    return {
        "requests": [
            {
                "image": {"content": content},
                "features": [{"type": "TEXT_DETECTION"}],
            }
        ]
    }


def run_stored_document_ocr(document: Dict[str, Any]) -> str:
    api_key = os.environ.get("GOOGLE_VISION_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_VISION_API_KEY is required")

    payload = _build_request(document)
    response = requests.post(
        GOOGLE_VISION_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    result = response.json()
    annotations = result.get("responses", [{}])[0]
    if "error" in annotations:
        raise RuntimeError(annotations["error"].get("message", "OCR failed"))
    return annotations.get("fullTextAnnotation", {}).get("text", "")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python stored_document_ocr.py <stored_document_json>")
    document = _load_document_payload(sys.argv[1])
    print(run_stored_document_ocr(document))


if __name__ == "__main__":
    main()
