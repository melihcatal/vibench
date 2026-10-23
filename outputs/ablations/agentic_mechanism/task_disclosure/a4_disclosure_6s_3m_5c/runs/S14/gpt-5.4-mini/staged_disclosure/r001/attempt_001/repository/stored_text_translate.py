import os
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _get_env(name: str, default: str = "") -> str:
    value = os.environ.get(name, default)
    if value is None:
        return default
    return value


def _extract_text_from_document(document: Any) -> str:
    if isinstance(document, str):
        return document
    if isinstance(document, dict):
        for key in ("text", "content", "body", "document_text", "stored_text"):
            value = document.get(key)
            if isinstance(value, str) and value.strip():
                return value
        for key in ("pages", "segments", "chunks", "items"):
            value = document.get(key)
            if isinstance(value, list):
                parts = []
                for item in value:
                    if isinstance(item, str):
                        parts.append(item)
                    elif isinstance(item, dict):
                        for nested_key in ("text", "content", "body"):
                            nested_value = item.get(nested_key)
                            if isinstance(nested_value, str) and nested_value.strip():
                                parts.append(nested_value)
                                break
                combined = "\n".join(part for part in parts if part.strip())
                if combined.strip():
                    return combined
    raise ValueError("No extractable text found in stored document")


def translate_stored_document(document: Any, target_language: str = "English") -> Dict[str, Any]:
    source_text = _extract_text_from_document(document)
    api_key = _get_env("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": f"You translate text into {target_language} while preserving meaning, formatting, and line breaks."},
            {"role": "user", "content": source_text},
        ],
        "temperature": 0,
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
    translated_text = data["choices"][0]["message"]["content"]
    return {
        "source_text": source_text,
        "translated_text": translated_text,
        "provider": "openai",
        "model": OPENAI_MODEL,
    }
