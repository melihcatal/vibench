import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _extract_text(payload: Dict[str, Any]) -> str:
    if "text" in payload and isinstance(payload["text"], str):
        return payload["text"]
    if "content" in payload and isinstance(payload["content"], str):
        return payload["content"]
    if "document_text" in payload and isinstance(payload["document_text"], str):
        return payload["document_text"]
    if "extracted_text" in payload and isinstance(payload["extracted_text"], str):
        return payload["extracted_text"]
    raise ValueError("Missing source text to translate")


def _build_messages(text: str, target_language: str, source_language: Optional[str]) -> List[Dict[str, str]]:
    system_parts = ["You are a precise translation engine."]
    if source_language:
        system_parts.append(f"Translate from {source_language} to {target_language}.")
    else:
        system_parts.append(f"Translate the input to {target_language}.")
    system_parts.append("Preserve meaning, tone, formatting, and line breaks when possible.")
    return [
        {"role": "system", "content": " ".join(system_parts)},
        {"role": "user", "content": text},
    ]


def translate_stored_text(
    payload: Dict[str, Any],
    target_language: str,
    source_language: Optional[str] = None,
) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    text = _extract_text(payload)
    if not text.strip():
        raise ValueError("Source text is empty")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": _build_messages(text, target_language, source_language),
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    translated_text = data["choices"][0]["message"]["content"]
    return {
        "source_text": text,
        "translated_text": translated_text,
        "target_language": target_language,
        "source_language": source_language,
        "model": OPENAI_MODEL,
        "provider": "openai",
    }
