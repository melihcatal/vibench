import json
import os
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def extract_key_values(document_text: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract key-value pairs from form-like documents and return only a JSON object mapping field names to values.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": document_text}
                ],
            },
        ],
        "text": {"format": {"type": "json_object"}},
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text += content.get("text", "")

    if not text:
        raise ValueError("No extracted content returned by OpenAI API")

    return json.loads(text)


def main() -> None:
    import sys

    document_text = sys.stdin.read()
    result = extract_key_values(document_text)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
