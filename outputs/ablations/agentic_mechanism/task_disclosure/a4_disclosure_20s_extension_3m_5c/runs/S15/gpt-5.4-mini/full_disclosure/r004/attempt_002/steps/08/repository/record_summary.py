import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _normalize_record(record: Any) -> Dict[str, Any]:
    if isinstance(record, dict):
        return record
    if isinstance(record, str):
        try:
            parsed = json.loads(record)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            return {"text": record}
    return {"value": record}


def _compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True, default=str)


def summarize_record(record: Any, max_chars: int = 1200) -> str:
    normalized = _normalize_record(record)
    payload = _compact_json(normalized)
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")
    if len(payload) > max_chars:
        payload = payload[:max_chars]

    url = f"{OPENAI_API_BASE.rstrip('/')}/responses"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": "Summarize retrieved document records concisely and faithfully.",
            },
            {
                "role": "user",
                "content": f"Summarize this document record in 1-3 sentences:\n{payload}",
            },
        ],
    }
    response = requests.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    data = response.json()
    output = data.get("output", [])
    texts: List[str] = []
    for item in output:
        content = item.get("content", []) if isinstance(item, dict) else []
        for part in content:
            if isinstance(part, dict):
                text = part.get("text")
                if text:
                    texts.append(text)
    if texts:
        return "\n".join(texts).strip()
    return json.dumps(data, ensure_ascii=False)
