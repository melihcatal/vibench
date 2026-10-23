from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "gpt-4.1-mini")


def _extract_text(payload: Dict[str, Any]) -> str:
    if isinstance(payload.get("text"), str):
        return payload["text"]
    if isinstance(payload.get("transcript"), str):
        return payload["transcript"]
    if isinstance(payload.get("content"), str):
        return payload["content"]
    raise ValueError("Expected transcript text in 'text', 'transcript', or 'content'.")


def _moderation_instructions() -> str:
    return (
        "You are a transcript moderation assistant. Clean the transcript for publishing while preserving meaning. "
        "Fix obvious transcription errors, remove profanity if necessary for a general audience, redact personal data, "
        "and avoid adding facts not present in the source. Return JSON with keys: moderated_text, notes, redactions. "
        "moderated_text must be the publishable transcript. notes must briefly describe changes. redactions must be a list of redacted items."
    )


def moderate_transcript(payload: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    transcript = _extract_text(payload)
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required.")

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": _moderation_instructions()},
                {"role": "user", "content": transcript},
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    if isinstance(content, str):
        return json.loads(content)
    return content
