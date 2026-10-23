import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-5.4-mini")


def _messages(text: str, schema: Optional[Dict[str, Any]] = None) -> List[Dict[str, str]]:
    system = "Extract structured JSON from the provided text. Return only valid JSON."
    if schema is not None:
        system += " Match this schema as closely as possible: " + json.dumps(schema, ensure_ascii=False)
    user = text
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def extract_json(text: str, schema: Optional[Dict[str, Any]] = None) -> Any:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": _messages(text, schema),
        "temperature": 0,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)
