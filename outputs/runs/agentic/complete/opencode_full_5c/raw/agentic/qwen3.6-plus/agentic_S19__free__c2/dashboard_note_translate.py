from __future__ import annotations

import os
from typing import Optional

import httpx

from observability_models import DashboardNote, TranslationResult

DEEPL_API_URL = "https://api.deepl.com"
DEEPL_TRANSLATE_ENDPOINT = "/v2/translate"
ENV_DEEPL_API_KEY = "DEEPL_AUTH_KEY"


def _get_deepl_api_key() -> str:
    api_key = os.environ.get(ENV_DEEPL_API_KEY, "")
    if not api_key:
        raise ValueError(
            f"DeepL API key is required. Set {ENV_DEEPL_API_KEY} environment variable."
        )
    return api_key


def dashboard_note_translate(
    note: DashboardNote,
    target_language: str = "en",
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
) -> TranslationResult:
    api_key = api_key or _get_deepl_api_key()

    text_to_translate = note.note_text

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = {
        "text": text_to_translate,
        "target_lang": target_language.upper(),
    }
    if source_language:
        payload["source_lang"] = source_language.upper()

    response = httpx.post(
        url=f"{DEEPL_API_URL}{DEEPL_TRANSLATE_ENDPOINT}",
        headers=headers,
        data=payload,
        timeout=15.0,
    )
    response.raise_for_status()
    result_data = response.json()

    translations = result_data.get("translations", [])
    if not translations:
        return TranslationResult(
            original_text=text_to_translate,
            translated_text=text_to_translate,
            source_language=source_language or "auto",
            target_language=target_language,
            provider="deepl",
        )

    translation_entry = translations[0]
    translated_text = translation_entry.get("text", text_to_translate)
    detected_source = translation_entry.get(
        "detected_source_language", source_language or "auto"
    )

    return TranslationResult(
        original_text=text_to_translate,
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_language,
        provider="deepl",
    )


def translate_dashboard_note_text(
    note_text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
) -> TranslationResult:
    note = DashboardNote(note_text=note_text)
    return dashboard_note_translate(
        note=note,
        target_language=target_language,
        source_language=source_language,
        api_key=api_key,
    )
