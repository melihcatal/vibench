import os
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_text(asset: Any) -> str:
    if isinstance(asset, str):
        return asset
    if isinstance(asset, bytes):
        return asset.decode("utf-8", errors="replace")
    if isinstance(asset, dict):
        for key in ("text", "content", "summary", "body"):
            value = asset.get(key)
            if isinstance(value, str):
                return value
            if isinstance(value, bytes):
                return value.decode("utf-8", errors="replace")
    raise TypeError("Unsupported stored asset object")


def summarize_stored_asset(asset: Any, max_tokens: int = 180) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OpenAI API key")

    text = _extract_text(asset)
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "Summarize stored asset content concisely."},
                {"role": "user", "content": text},
            ],
            "max_tokens": max_tokens,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    choices = payload.get("choices", [])
    if not choices:
        raise RuntimeError("No summary returned by OpenAI")
    message = choices[0].get("message", {})
    summary = message.get("content", "")
    return {"summary": summary, "raw_response": payload}
