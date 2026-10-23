import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def extract_json(text: str, schema_hint: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")

    messages = [
        {
            "role": "system",
            "content": "Extract structured JSON from the provided text. Return only valid JSON.",
        },
        {
            "role": "user",
            "content": f"Schema hint: {schema_hint}\n\nText:\n{text}",
        },
    ]

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": messages,
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    content = payload["choices"][0]["message"]["content"]
    return json.loads(content)
