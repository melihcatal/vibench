from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import requests


DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class OCRTranslateRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None
    model: str = DEFAULT_OPENAI_MODEL


@dataclass(frozen=True)
class OCRTranslateResponse:
    translated_text: str
    raw: str


def _build_prompt(text: str, target_language: str, source_language: Optional[str]) -> str:
    source = f"from {source_language} " if source_language else ""
    return (
        f"Translate the following OCR-extracted text {source}to {target_language}. "
        "Preserve line breaks, numbers, names, addresses, and formatting as much as possible.\n\n"
        f"{text}"
    )


def translate_ocr_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = DEFAULT_OPENAI_MODEL,
    base_url: str = DEFAULT_OPENAI_BASE_URL,
    timeout: float = 60.0,
) -> OCRTranslateResponse:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a translation assistant for OCR text."},
            {"role": "user", "content": _build_prompt(text, target_language, source_language)},
        ],
        "temperature": 0,
    }
    response = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    translated_text = data["choices"][0]["message"]["content"].strip()
    return OCRTranslateResponse(translated_text=translated_text, raw=translated_text)
