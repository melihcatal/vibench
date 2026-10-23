from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping, Optional

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEFAULT_TIMEOUT_SECONDS = 30.0


@dataclass(frozen=True)
class DashboardNoteTranslationRequest:
    text: str
    target_lang: str
    source_lang: Optional[str] = None
    preserve_formatting: bool = True


@dataclass(frozen=True)
class DashboardNoteTranslationResult:
    text: str
    detected_source_lang: Optional[str]
    target_lang: str
    raw: dict[str, Any]


def _load_api_key() -> str:
    api_key = os.getenv("DEEPL_API_KEY") or os.getenv("DEEPL_AUTH_KEY") or ""
    if not api_key:
        raise ValueError("Missing DEEPL_API_KEY")
    return api_key


def _normalize_lang(lang: str) -> str:
    value = lang.strip()
    if not value:
        raise ValueError("target_lang must not be empty")
    return value.upper()


def translate_dashboard_note(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    preserve_formatting: bool = True,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
) -> DashboardNoteTranslationResult:
    api_key = _load_api_key()
    payload: dict[str, Any] = {
        "auth_key": api_key,
        "text": text,
        "target_lang": _normalize_lang(target_lang),
        "preserve_formatting": 1 if preserve_formatting else 0,
    }
    if source_lang:
        payload["source_lang"] = _normalize_lang(source_lang)
    response = requests.post(DEEPL_API_URL, data=payload, timeout=timeout_seconds)
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations") or []
    if not translations:
        raise ValueError("DeepL response did not include translations")
    first = translations[0]
    return DashboardNoteTranslationResult(
        text=str(first.get("text", "")),
        detected_source_lang=first.get("detected_source_language"),
        target_lang=_normalize_lang(target_lang),
        raw=dict(data),
    )


def translate_metric_or_dashboard_note(payload: Mapping[str, Any]) -> DashboardNoteTranslationResult:
    text = str(payload.get("text") or payload.get("note") or "")
    if not text:
        raise ValueError("payload must include text or note")
    target_lang = str(payload.get("target_lang") or payload.get("locale") or "")
    if not target_lang:
        raise ValueError("payload must include target_lang or locale")
    source_lang = payload.get("source_lang")
    preserve_formatting = bool(payload.get("preserve_formatting", True))
    timeout_raw = payload.get("timeout_seconds")
    timeout_seconds = float(timeout_raw) if timeout_raw is not None else DEFAULT_TIMEOUT_SECONDS
    return translate_dashboard_note(
        text=text,
        target_lang=target_lang,
        source_lang=str(source_lang) if source_lang else None,
        preserve_formatting=preserve_formatting,
        timeout_seconds=timeout_seconds,
    )
