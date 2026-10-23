import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _coerce_text(text: Any) -> str:
    if text is None:
        return ""
    if isinstance(text, str):
        return text
    if isinstance(text, list):
        parts: List[str] = []
        for item in text:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                value = item.get("text") or item.get("content") or item.get("value")
                if value:
                    parts.append(str(value))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    if isinstance(text, dict):
        value = text.get("text") or text.get("content") or text.get("value")
        return str(value) if value is not None else str(text)
    return str(text)


def translate_ocr_text(text: Any, target_language: str, source_language: Optional[str] = None, api_key: Optional[str] = None, temperature: float = 0.0) -> str:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    source_text = _coerce_text(text)
    if not source_text.strip():
        return ""

    system_prompt = "You translate OCR-extracted text faithfully. Preserve formatting, line breaks, numbers, names, addresses, and labels. Return only the translated text."
    if source_language:
        user_prompt = f"Translate the following OCR text from {source_language} to {target_language}:\n\n{source_text}"
    else:
        user_prompt = f"Translate the following OCR text to {target_language}:\n\n{source_text}"

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    content = message.get("content")
    return content if isinstance(content, str) else _coerce_text(content)


def translate_ocr_fields(fields: Dict[str, Any], target_language: str, source_language: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
    translated: Dict[str, Any] = {}
    for key, value in fields.items():
        if isinstance(value, str):
            translated[key] = translate_ocr_text(value, target_language, source_language=source_language, api_key=api_key)
        elif isinstance(value, dict):
            translated[key] = translate_ocr_fields(value, target_language, source_language=source_language, api_key=api_key)
        elif isinstance(value, list):
            translated[key] = [translate_ocr_fields(item, target_language, source_language=source_language, api_key=api_key) if isinstance(item, dict) else translate_ocr_text(item, target_language, source_language=source_language, api_key=api_key) if isinstance(item, str) else item for item in value]
        else:
            translated[key] = value
    return translated
