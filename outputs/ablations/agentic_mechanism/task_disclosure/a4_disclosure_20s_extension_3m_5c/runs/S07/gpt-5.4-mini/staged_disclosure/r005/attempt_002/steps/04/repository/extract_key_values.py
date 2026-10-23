import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _read_document(document_path: str) -> str:
    path = Path(document_path)
    if not path.is_file():
        raise FileNotFoundError(document_path)
    return path.read_text(encoding="utf-8", errors="ignore")


def _build_prompt() -> str:
    return (
        "Extract key-value pairs from the form-like document content. "
        'Return JSON only with this schema: {"key_values":[{"key":"","value":""}]}. '
        "Preserve the original key labels and normalize values to strings. "
        "If no key-value pairs exist, return {\"key_values\":[]}."
    )


def extract_key_values(document_path: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    document_text = _read_document(document_path)
    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": _build_prompt()},
                    {"type": "input_text", "text": document_text},
                ],
            }
        ],
        "response_format": {"type": "json_object"},
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text += content.get("text", "")

    if not text:
        return data

    return json.loads(text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python extract_key_values.py <document_path>")
    print(json.dumps(extract_key_values(sys.argv[1]), ensure_ascii=False))
