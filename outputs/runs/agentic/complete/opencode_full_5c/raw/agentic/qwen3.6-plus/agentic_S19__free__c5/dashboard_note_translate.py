from typing import Optional

import requests

from observability_client import (
    DEEPL_API_BASE,
    create_deepl_session,
    validate_deepl_credentials,
)
from observability_models import (
    DashboardNote,
    TranslationResult,
)


def dashboard_note_translate(
    note: DashboardNote,
) -> TranslationResult:
    if not validate_deepl_credentials():
        raise ValueError(
            "DeepL API key not configured. Set DEEPL_API_KEY environment variable."
        )

    api_url = f"{DEEPL_API_BASE}/v2/translate"

    source_lang = note.source_locale.upper()
    target_lang = note.target_locale.upper()

    if source_lang == "EN":
        source_lang = "EN-US"
    if target_lang == "PT":
        target_lang = "PT-BR"
    elif target_lang == "ES":
        target_lang = "ES"
    elif target_lang == "FR":
        target_lang = "FR"
    elif target_lang == "DE":
        target_lang = "DE"
    elif target_lang == "JA":
        target_lang = "JA"
    elif target_lang == "ZH":
        target_lang = "ZH"

    payload = {
        "text": note.note_text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "tag_handling": "xml",
        "ignore_tags": "metric,resource",
    }

    session = create_deepl_session()
    response = session.post(api_url, data=payload, timeout=30)
    response.raise_for_status()

    result_data = response.json()
    translations = result_data.get("translations", [])

    if not translations:
        raise ValueError("DeepL API returned no translations.")

    translated_text = translations[0].get("text", "")
    detected_source = translations[0].get(
        "detected_source_language", note.source_locale
    )

    confidence = 1.0 if detected_source == source_lang[:2] else 0.8

    return TranslationResult(
        original_note=note,
        translated_text=translated_text,
        source_locale=note.source_locale,
        target_locale=note.target_locale,
        confidence=confidence,
    )


def translate_note_text(
    note_text: str,
    source_locale: str = "en",
    target_locale: str = "es",
    dashboard_id: Optional[str] = None,
) -> TranslationResult:
    note = DashboardNote(
        note_text=note_text,
        dashboard_id=dashboard_id,
        source_locale=source_locale,
        target_locale=target_locale,
    )
    return dashboard_note_translate(note)
