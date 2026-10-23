import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


def _build_headers() -> Dict[str, str]:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise ValueError(f"Missing required environment variable: {OPENAI_API_KEY_ENV}")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def translate_ocr_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    if not text:
        return ""

    system_prompt = (
        "You translate OCR-extracted text accurately while preserving line breaks, punctuation, "
        "and document structure. Return only the translated text."
    )
    user_parts: List[str] = []
    if source_language:
        user_parts.append(f"Source language: {source_language}")
    user_parts.append(f"Target language: {target_language}")
    user_parts.append("Text:")
    user_parts.append(text)

    payload: Dict[str, Any] = {
        "model": OPENAI_TRANSLATION_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "\n".join(user_parts)},
        ],
        "temperature": 0,
    }

    response = requests.post(
        f"{OPENAI_API_BASE}/chat/completions",
        headers=_build_headers(),
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def translate_ocr_batch(
    texts: List[str], target_language: str, source_language: Optional[str] = None
) -> List[str]:
    return [translate_ocr_text(text, target_language, source_language) for text in texts]
