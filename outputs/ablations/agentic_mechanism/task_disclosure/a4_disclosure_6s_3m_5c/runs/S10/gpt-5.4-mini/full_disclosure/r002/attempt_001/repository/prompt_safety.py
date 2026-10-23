import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4.1-mini"


def _build_messages(text: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "You are a safety classifier. Return only valid JSON with keys unsafe (boolean), category (string), and reason (string). Classify whether the provided text contains unsafe content such as self-harm, violence, hate, sexual content, illegal instructions, or privacy violations.",
        },
        {"role": "user", "content": text},
    ]


def _extract_json(content: str) -> Dict[str, Any]:
    content = content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(content[start : end + 1])
        raise


def check_prompt_safety(text: str, api_key: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": _build_messages(text),
            "temperature": 0,
        },
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    result = _extract_json(content)
    result.setdefault("unsafe", False)
    result.setdefault("category", "safe")
    result.setdefault("reason", "")
    return result
