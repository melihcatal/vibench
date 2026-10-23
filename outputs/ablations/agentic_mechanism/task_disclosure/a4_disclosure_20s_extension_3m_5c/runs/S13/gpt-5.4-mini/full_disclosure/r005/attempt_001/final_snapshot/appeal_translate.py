from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1").rstrip("/")
OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


@dataclass(frozen=True)
class AppealTranslationResult:
    translated_text: str
    source_language: Optional[str]
    target_language: str
    raw: Dict[str, Any]


def _require_api_key() -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")
    return OPENAI_API_KEY


def translate_appeal_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    model: str = OPENAI_TRANSLATION_MODEL,
    timeout: int = 30,
) -> AppealTranslationResult:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(target_language, str) or not target_language.strip():
        raise ValueError("target_language must be a non-empty string")
    _require_api_key()

    system_prompt = (
        "You translate moderation appeal text for review. "
        "Return only the translated text, preserving meaning, tone, names, numbers, and formatting."
    )
    if source_language:
        user_prompt = f"Translate this appeal from {source_language} to {target_language}:\n{text}"
    else:
        user_prompt = f"Translate this appeal to {target_language}:\n{text}"

    response = requests.post(
        f"{OPENAI_API_BASE}/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
        },
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    translated_text = ""
    choices = data.get("choices") if isinstance(data, dict) else None
    if isinstance(choices, list) and choices:
        choice = choices[0]
        if isinstance(choice, dict):
            message = choice.get("message")
            if isinstance(message, dict):
                translated_text = str(message.get("content", "")).strip()

    return AppealTranslationResult(
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
        raw=data if isinstance(data, dict) else {},
    )
