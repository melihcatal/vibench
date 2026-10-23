import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def extract_json(text: str, schema_hint: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    instructions = "Extract the structured JSON from the provided text. Return only valid JSON."
    if schema_hint:
        instructions = f"{instructions} Follow this schema hint: {schema_hint}"

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": instructions},
            {"role": "user", "content": text},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    if isinstance(content, str):
        return json.loads(content)
    return content
