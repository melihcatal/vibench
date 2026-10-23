from typing import Dict

import requests

ANTHROPIC_API_KEY = __import__("os").getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"


def extract_structured_fields(normalized_text: str, api_key: str = "") -> Dict[str, object]:
    key = api_key or ANTHROPIC_API_KEY
    if not key:
        raise ValueError("Anthropic API key is required")
    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": f"Extract structured fields as JSON from this OCR text:\n{normalized_text}"}
        ],
    }
    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()
