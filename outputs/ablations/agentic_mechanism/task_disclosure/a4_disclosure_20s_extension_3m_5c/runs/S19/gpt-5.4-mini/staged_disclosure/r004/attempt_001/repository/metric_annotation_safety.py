import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_prompt(text: str) -> str:
    return (
        "Check the following metric label or annotation for unsafe text. "
        "Unsafe text includes hate, harassment, sexual content, self-harm, violent threats, "
        "illicit instructions, or highly toxic language. Return only valid JSON with keys "
        "unsafe (boolean) and reasons (array of strings). Text: "
        f"{text}"
    )


def check_metric_annotation_safety(text: str, api_key: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a strict text safety classifier."},
            {"role": "user", "content": _build_prompt(text)},
        ],
        "temperature": 0,
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return {"provider": "openai", "model": OPENAI_MODEL, "raw": content}


def is_metric_annotation_safe(text: str, api_key: Optional[str] = None, timeout: int = 30) -> bool:
    result = check_metric_annotation_safety(text, api_key=api_key, timeout=timeout)
    raw = result.get("raw", "")
    lowered = raw.lower()
    return '"unsafe": true' not in lowered and "'unsafe': true" not in lowered
