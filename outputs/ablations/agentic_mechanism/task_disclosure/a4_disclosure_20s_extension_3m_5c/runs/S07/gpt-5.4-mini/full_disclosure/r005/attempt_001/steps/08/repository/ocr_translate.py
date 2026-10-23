import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_TRANSLATE_MODEL", "gpt-4.1-mini")


def _coerce_text(input_text: Any) -> str:
    if input_text is None:
        return ""
    if isinstance(input_text, str):
        return input_text
    if isinstance(input_text, list):
        parts: List[str] = []
        for item in input_text:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                for key in ("text", "content", "value"):
                    if key in item and item[key] is not None:
                        parts.append(str(item[key]))
                        break
        return "\n".join(parts)
    if isinstance(input_text, dict):
        for key in ("text", "content", "value"):
            if key in input_text and input_text[key] is not None:
                return str(input_text[key])
    return str(input_text)


def translate_ocr_text(text: Any, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OCR translation")

    source = _coerce_text(text)
    if not source.strip():
        return ""

    system_prompt = "You translate OCR-extracted text faithfully while preserving structure, names, numbers, and line breaks."
    user_prompt = f"Translate the following text to {target_language}."
    if source_language:
        user_prompt += f" The source language is {source_language}."
    user_prompt += " Return only the translated text.\n\n" + source

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    return str(message.get("content") or "").strip()


def translate_document_ocr(result: Any, target_language: str, source_language: Optional[str] = None) -> Dict[str, Any]:
    translated_text = translate_ocr_text(result, target_language=target_language, source_language=source_language)
    return {
        "translated_text": translated_text,
        "target_language": target_language,
        "source_language": source_language,
    }
