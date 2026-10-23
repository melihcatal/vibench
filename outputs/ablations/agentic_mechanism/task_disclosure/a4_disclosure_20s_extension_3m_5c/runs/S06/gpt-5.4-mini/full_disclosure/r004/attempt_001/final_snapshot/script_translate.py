from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional

from openai import OpenAI


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None
    model: str = "gpt-4o-mini"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TranslationResponse:
    text: str
    target_language: str
    source_language: Optional[str] = None
    model: str = "gpt-4o-mini"
    metadata: Dict[str, Any] = field(default_factory=dict)


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def _normalize_metadata(value: Any) -> Dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def normalize_translation_request(payload: Mapping[str, Any] | TranslationRequest) -> TranslationRequest:
    if isinstance(payload, TranslationRequest):
        return TranslationRequest(
            text=_normalize_text(payload.text),
            target_language=_normalize_text(payload.target_language),
            source_language=_normalize_text(payload.source_language) or None,
            model=_normalize_text(payload.model) or "gpt-4o-mini",
            metadata=_normalize_metadata(payload.metadata),
        )
    return TranslationRequest(
        text=_normalize_text(payload.get("text", "")),
        target_language=_normalize_text(payload.get("target_language", "")),
        source_language=_normalize_text(payload.get("source_language")) or None,
        model=_normalize_text(payload.get("model", "gpt-4o-mini")) or "gpt-4o-mini",
        metadata=_normalize_metadata(payload.get("metadata", {})),
    )


def normalize_translation_response(payload: Mapping[str, Any] | TranslationResponse) -> TranslationResponse:
    if isinstance(payload, TranslationResponse):
        return TranslationResponse(
            text=_normalize_text(payload.text),
            target_language=_normalize_text(payload.target_language),
            source_language=_normalize_text(payload.source_language) or None,
            model=_normalize_text(payload.model) or "gpt-4o-mini",
            metadata=_normalize_metadata(payload.metadata),
        )
    return TranslationResponse(
        text=_normalize_text(payload.get("text", "")),
        target_language=_normalize_text(payload.get("target_language", "")),
        source_language=_normalize_text(payload.get("source_language")) or None,
        model=_normalize_text(payload.get("model", "gpt-4o-mini")) or "gpt-4o-mini",
        metadata=_normalize_metadata(payload.get("metadata", {})),
    )


def load_translation_client() -> OpenAI:
    kwargs: Dict[str, Any] = {}
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    organization = os.getenv("OPENAI_ORG_ID")
    project = os.getenv("OPENAI_PROJECT_ID")
    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        kwargs["base_url"] = base_url
    if organization:
        kwargs["organization"] = organization
    if project:
        kwargs["project"] = project
    return OpenAI(**kwargs)


def translate_script(request: Mapping[str, Any] | TranslationRequest) -> TranslationResponse:
    normalized = normalize_translation_request(request)
    client = load_translation_client()
    prompt = [
        "Translate the narration script to the target language while preserving meaning, tone, line breaks, names, and formatting.",
        f"Target language: {normalized.target_language}",
    ]
    if normalized.source_language:
        prompt.append(f"Source language: {normalized.source_language}")
    prompt.append("Return only the translated script text.")
    result = client.responses.create(
        model=normalized.model or "gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": "You are a careful translation engine for narration scripts.",
            },
            {
                "role": "user",
                "content": "\n".join(prompt) + "\n\n" + normalized.text,
            },
        ],
    )
    translated = _normalize_text(getattr(result, "output_text", ""))
    return TranslationResponse(
        text=translated,
        target_language=normalized.target_language,
        source_language=normalized.source_language,
        model=normalized.model or "gpt-4o-mini",
        metadata={"provider": "openai"},
    )
