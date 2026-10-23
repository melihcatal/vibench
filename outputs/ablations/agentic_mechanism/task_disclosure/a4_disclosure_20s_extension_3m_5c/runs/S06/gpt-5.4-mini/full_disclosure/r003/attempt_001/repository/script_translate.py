from __future__ import annotations

import os
from typing import Optional

import requests


OPENAI_TRANSLATE_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_TRANSLATE_MODEL = "gpt-4o-mini"


def translate_script(text: str, target_language: str, source_language: Optional[str] = None, api_key: Optional[str] = None, model: str = OPENAI_TRANSLATE_MODEL, timeout: int = 120) -> str:
    resolved_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not resolved_api_key:
        raise ValueError("OPENAI_API_KEY is required")
    if not text:
        return ""
    language_instruction = f"Translate the narration script into {target_language}."
    if source_language:
        language_instruction = f"Translate the narration script from {source_language} into {target_language}."
    response = requests.post(
        OPENAI_TRANSLATE_API_URL,
        headers={"Authorization": f"Bearer {resolved_api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You translate narration scripts accurately and naturally."},
                {"role": "user", "content": f"{language_instruction} Preserve meaning, tone, and punctuation. Return only the translated script.\n\n{text}"},
            ],
            "temperature": 0,
        },
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
