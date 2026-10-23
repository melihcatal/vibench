from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

import requests


OPENAI_CHAT_API_HOST = "https://api.openai.com/v1/chat/completions"
OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


@dataclass(frozen=True)
class TranslationRequest:
    query: str
    target_language: str = "en"
    source_language: str | None = None
    model: str = OPENAI_TRANSLATION_MODEL

    def to_messages(self) -> list[dict[str, str]]:
        system = (
            "You translate user search queries for multilingual embedding search. "
            "Return only the translated query text with no quotes, notes, or extra formatting."
        )
        parts = [f"Translate the following query into {self.target_language}."]
        if self.source_language:
            parts.append(f"The source language is {self.source_language}.")
        parts.append(f"Query: {self.query}")
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": " ".join(parts)},
        ]


@dataclass(frozen=True)
class TranslationResult:
    translated_query: str
    model: str | None = None
    raw_response: Mapping[str, Any] | None = None


def _resolve_api_key(api_key: str | None = None) -> str:
    resolved = api_key or os.getenv("OPENAI_API_KEY")
    if not resolved:
        raise RuntimeError("OPENAI_API_KEY is required")
    return resolved


def translate_query(
    query: str,
    target_language: str = "en",
    source_language: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
    timeout: float = 60.0,
) -> TranslationResult:
    request = TranslationRequest(
        query=query,
        target_language=target_language,
        source_language=source_language,
        model=model or OPENAI_TRANSLATION_MODEL,
    )
    response = requests.post(
        OPENAI_CHAT_API_HOST,
        headers={"Authorization": f"Bearer {_resolve_api_key(api_key)}", "Content-Type": "application/json"},
        json={"model": request.model, "messages": request.to_messages(), "temperature": 0},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    choices: Sequence[Mapping[str, Any]] = payload.get("choices", [])
    translated = ""
    if choices:
        message = choices[0].get("message", {})
        translated = str(message.get("content", "")).strip()
    return TranslationResult(translated_query=translated, model=payload.get("model"), raw_response=payload)
