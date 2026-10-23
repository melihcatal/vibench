import json
import os
import sys
from typing import Any

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def _extract_input_text(payload: dict[str, Any]) -> str:
    if isinstance(payload.get("output_text"), str) and payload["output_text"].strip():
        return payload["output_text"]
    outputs = payload.get("output", [])
    parts = []
    for item in outputs:
        if isinstance(item, dict):
            for content in item.get("content", []):
                if isinstance(content, dict) and content.get("type") in {"output_text", "text"}:
                    text = content.get("text")
                    if isinstance(text, str):
                        parts.append(text)
    return "".join(parts)


def extract_json(text: str) -> Any:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract the structured data from the user's text and return only valid JSON. Do not include markdown or commentary.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text},
                    ],
                },
            ],
            "text": {"format": {"type": "json_object"}},
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    output_text = _extract_input_text(data).strip()
    if not output_text:
        raise RuntimeError("No JSON returned by OpenAI")
    return json.loads(output_text)


def main() -> None:
    text = sys.stdin.read()
    if not text.strip() and len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    result = extract_json(text)
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
