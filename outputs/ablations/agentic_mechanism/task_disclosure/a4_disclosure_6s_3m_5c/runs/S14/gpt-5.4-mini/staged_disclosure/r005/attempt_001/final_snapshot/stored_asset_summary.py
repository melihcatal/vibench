import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_text(asset: Any) -> str:
    if asset is None:
        return ""
    if isinstance(asset, str):
        return asset.strip()
    if isinstance(asset, dict):
        for key in ("content", "text", "body", "summary", "extracted_text"):
            value = asset.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        parts: List[str] = []
        for value in asset.values():
            if isinstance(value, str) and value.strip():
                parts.append(value.strip())
        return "\n".join(parts).strip()
    if isinstance(asset, list):
        parts = [_extract_text(item) for item in asset]
        return "\n".join(part for part in parts if part).strip()
    return str(asset).strip()


def summarize_stored_asset(asset: Any, max_summary_words: int = 120) -> str:
    text = _extract_text(asset)
    if not text:
        return ""

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        prompt = (
            "Summarize the following extracted asset content clearly and concisely. "
            f"Keep the summary under {max_summary_words} words.\n\n"
            f"Content:\n{text}"
        )
        payload: Dict[str, Any] = {
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a concise summarization assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "max_tokens": max(64, max_summary_words * 2),
        }
        response = requests.post(
            OPENAI_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        choices = data.get("choices", [])
        if choices:
            message = choices[0].get("message", {})
            content = message.get("content", "")
            if isinstance(content, str):
                return content.strip()

    words = text.split()
    if len(words) <= max_summary_words:
        return text
    return " ".join(words[:max_summary_words]).rstrip() + "..."


if __name__ == "__main__":
    import json
    import sys

    source = sys.stdin.read()
    try:
        parsed = json.loads(source) if source.strip() else source
    except json.JSONDecodeError:
        parsed = source
    print(summarize_stored_asset(parsed))
