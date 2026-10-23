from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

import requests


OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-5.4-mini"


def _env(name: str, fallback: Optional[str] = None) -> Optional[str]:
    value = os.environ.get(name)
    if value:
        return value
    return fallback


@dataclass(frozen=True)
class DashboardNoteTranslationRequest:
    text: str
    target_locale: str
    source_locale: str | None = None
    tone: str | None = None

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "DashboardNoteTranslationRequest":
        return cls(
            text=str(payload["text"]),
            target_locale=str(payload["target_locale"]),
            source_locale=str(payload["source_locale"]) if payload.get("source_locale") is not None else None,
            tone=str(payload["tone"]) if payload.get("tone") is not None else None,
        )


@dataclass(frozen=True)
class DashboardNoteTranslationResult:
    source_text: str
    translated_text: str
    target_locale: str
    source_locale: str | None = None


class OpenAIDashboardNoteTranslator:
    def __init__(self, api_key: Optional[str] = None, model: str = OPENAI_MODEL, timeout_seconds: int = 30):
        self.api_key = api_key or _env("OPENAI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("OPENAI_API_KEY is required")
        self.model = model
        self.timeout_seconds = timeout_seconds

    def translate(self, request: DashboardNoteTranslationRequest) -> DashboardNoteTranslationResult:
        messages = [
            {
                "role": "system",
                "content": "You translate observability dashboard and metric notes accurately while preserving numbers, labels, and markdown-like formatting.",
            },
            {
                "role": "user",
                "content": self._build_prompt(request),
            },
        ]
        response = requests.post(
            f"{OPENAI_API_BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": messages,
                "temperature": 0,
            },
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        translated_text = data["choices"][0]["message"]["content"].strip()
        return DashboardNoteTranslationResult(
            source_text=request.text,
            translated_text=translated_text,
            target_locale=request.target_locale,
            source_locale=request.source_locale,
        )

    def _build_prompt(self, request: DashboardNoteTranslationRequest) -> str:
        parts = [f"Translate the following note into {request.target_locale}."]
        if request.source_locale:
            parts.append(f"Source locale: {request.source_locale}.")
        if request.tone:
            parts.append(f"Tone: {request.tone}.")
        parts.append("Return only the translated text.")
        parts.append("")
        parts.append(request.text)
        return "\n".join(parts)


def translate_dashboard_note(payload: dict[str, Any]) -> dict[str, Any]:
    request = DashboardNoteTranslationRequest.from_payload(payload)
    translator = OpenAIDashboardNoteTranslator()
    result = translator.translate(request)
    return {
        "source_text": result.source_text,
        "translated_text": result.translated_text,
        "target_locale": result.target_locale,
        "source_locale": result.source_locale,
    }
