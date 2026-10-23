import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_CHAT_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_CHAT_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini")


def _resolve_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return key


def summarize_moderation(decisions: List[Dict[str, Any]], api_key: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    if not isinstance(decisions, list):
        raise TypeError("decisions must be a list")
    if any(not isinstance(decision, dict) for decision in decisions):
        raise TypeError("each decision must be a dictionary")

    key = _resolve_api_key(api_key)
    summary_model = model or OPENAI_CHAT_MODEL
    prompt = (
        "Summarize these moderation decisions for a reviewer. "
        "Highlight overall risk, notable categories, and any patterns. "
        f"Decisions: {decisions}"
    )
    response = requests.post(
        OPENAI_CHAT_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": summary_model,
            "messages": [
                {"role": "system", "content": "You summarize moderation outcomes concisely and clearly."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices") or []
    message = (choices[0].get("message") or {}) if choices else {}
    return {
        "provider": "openai",
        "model": summary_model,
        "summary": message.get("content", ""),
        "raw": data,
    }
