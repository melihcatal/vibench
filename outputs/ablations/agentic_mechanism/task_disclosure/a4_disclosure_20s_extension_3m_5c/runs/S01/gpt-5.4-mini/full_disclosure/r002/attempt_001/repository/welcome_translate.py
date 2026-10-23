import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def translate_onboarding_copy(text: str, locale: str, source_language: Optional[str] = None) -> str:
    if not text:
        return ""
    if not locale:
        raise ValueError("locale is required")

    system_prompt = "Translate onboarding copy accurately and naturally. Preserve product names, placeholders, markdown, and tone. Return only the translated text."
    user_prompt = f"Target locale: {locale}\n"
    if source_language:
        user_prompt += f"Source language: {source_language}\n"
    user_prompt += f"\nText:\n{text}"

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
    }

    response = requests.post(OPENAI_API_URL, headers=_headers(), json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    choices: List[Dict[str, Any]] = data.get("choices", [])
    if not choices:
        raise RuntimeError("OpenAI translation response missing choices")
    message = choices[0].get("message", {})
    content = message.get("content")
    if not isinstance(content, str):
        raise RuntimeError("OpenAI translation response missing content")
    return content.strip()


def translate_onboarding_copy_batch(texts: List[str], locale: str, source_language: Optional[str] = None) -> List[str]:
    return [translate_onboarding_copy(text, locale, source_language=source_language) for text in texts]
