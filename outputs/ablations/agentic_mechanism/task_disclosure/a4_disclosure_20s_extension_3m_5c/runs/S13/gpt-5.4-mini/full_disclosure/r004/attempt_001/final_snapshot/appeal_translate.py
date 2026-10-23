import os
from typing import Any, Dict, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def appeal_translate(text: str, target_language: str, api_key: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(target_language, str) or not target_language.strip():
        raise TypeError("target_language must be a non-empty string")

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

    selected_model = model or OPENAI_TRANSLATION_MODEL
    messages = [
        {"role": "system", "content": "Translate appeal text faithfully for moderation review. Preserve meaning, tone, names, numbers, and formatting. Return only the translation."},
        {"role": "user", "content": f"Target language: {target_language.strip()}\n\nAppeal text:\n{text}"},
    ]
    payload = {"model": selected_model, "messages": messages, "temperature": 0}
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices") or []
    translated_text = ""
    if choices:
        translated_text = ((choices[0].get("message") or {}).get("content") or "").strip()
    return {"provider": "openai", "model": selected_model, "target_language": target_language, "translated_text": translated_text, "raw": data}
