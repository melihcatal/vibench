import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def _extract_text(input_text: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": (
                    "Identify unsafe spans in the provided text. Return strict JSON with keys "
                    "unsafe_spans and redacted_text. unsafe_spans must be a list of objects with "
                    "start, end, label, and reason. redacted_text must replace unsafe spans with [REDACTED]."
                ),
            },
            {"role": "user", "content": input_text},
        ],
        "text": {"format": {"type": "json_object"}},
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    text = ""
    if isinstance(data.get("output"), list):
        for item in data["output"]:
            if isinstance(item, dict) and item.get("type") == "message":
                for part in item.get("content", []):
                    if isinstance(part, dict) and part.get("type") == "output_text":
                        text += part.get("text", "")
    if not text:
        text = data.get("output_text", "")
    return text


def redact_unsafe(text: str) -> Dict[str, Any]:
    raw = _extract_text(text)
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"unsafe_spans": [], "redacted_text": text}
    if "redacted_text" not in result:
        result["redacted_text"] = text
    if "unsafe_spans" not in result or not isinstance(result["unsafe_spans"], list):
        result["unsafe_spans"] = []
    return result


def main() -> None:
    import sys

    input_text = sys.stdin.read()
    result = redact_unsafe(input_text)
    sys.stdout.write(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
