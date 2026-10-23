from __future__ import annotations

import os
from typing import Any, Dict, Mapping, Optional

from openai import OpenAI


OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-5.4-mini")


def _get_api_key(api_key: Optional[str] = None) -> str:
    resolved = api_key or os.getenv("OPENAI_API_KEY")
    if not resolved:
        raise RuntimeError("OPENAI_API_KEY is required")
    return resolved


def _normalize_appeal(value: Any) -> Dict[str, Any]:
    if isinstance(value, str):
        return {"text": value}
    if isinstance(value, Mapping):
        return {"text": str(value.get("text", "")), "source_language": value.get("source_language"), "target_language": value.get("target_language")}
    raise TypeError("Unsupported appeal input type")


def translate_appeal_text(appeal: Any, target_language: str = "English", api_key: Optional[str] = None, model: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    normalized = _normalize_appeal(appeal)
    source_text = normalized["text"]
    source_language = normalized.get("source_language")
    resolved_target = normalized.get("target_language") or target_language
    client = OpenAI(api_key=_get_api_key(api_key))
    prompt = (
        "Translate the following appeal text for human moderation review. "
        "Preserve meaning, tone, and any factual details. Do not add commentary or analysis. "
        f"Target language: {resolved_target}."
    )
    if source_language:
        prompt += f" Source language: {source_language}."
    response = client.chat.completions.create(
        model=model or OPENAI_TRANSLATION_MODEL,
        messages=[
            {"role": "system", "content": "You are a precise translation assistant for moderation operations."},
            {"role": "user", "content": f"{prompt}\n\nAppeal text:\n{source_text}"},
        ],
        temperature=0,
        timeout=timeout,
    )
    translated_text = response.choices[0].message.content or ""
    return {
        "model": model or OPENAI_TRANSLATION_MODEL,
        "source_text": source_text,
        "translated_text": translated_text,
        "target_language": resolved_target,
    }
