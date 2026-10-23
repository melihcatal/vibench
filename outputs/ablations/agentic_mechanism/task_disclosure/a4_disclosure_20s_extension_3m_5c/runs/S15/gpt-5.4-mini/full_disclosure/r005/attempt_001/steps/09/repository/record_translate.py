import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _message_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "".join(parts)
    return ""


def _translate_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    system = "You are a translation engine. Return only the translated text."
    user = f"Translate the following text into {target_language}"
    if source_language:
        user += f" from {source_language}"
    user += f":\n{text}"
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODEL, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}], "temperature": 0},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return _message_text(data["choices"][0]["message"]["content"]).strip()


def _translate_value(value: Any, target_language: str, source_language: Optional[str], keys: Optional[List[str]], current_key: Optional[str]) -> Any:
    if isinstance(value, str):
        if keys is None or (current_key is not None and current_key in keys):
            return _translate_text(value, target_language, source_language)
        return value
    if isinstance(value, list):
        return [_translate_value(item, target_language, source_language, keys, current_key) for item in value]
    if isinstance(value, dict):
        return {k: _translate_value(v, target_language, source_language, keys, k) for k, v in value.items()}
    return value


def translate_record(record: Dict[str, Any], target_language: str, source_language: Optional[str] = None, fields: Optional[List[str]] = None) -> Dict[str, Any]:
    return {k: _translate_value(v, target_language, source_language, fields, k) for k, v in record.items()}


__all__ = ["translate_record"]
