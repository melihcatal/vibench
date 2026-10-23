from __future__ import annotations

from observability_client import deepl_translator
from observability_models import TranslationResponse


def dashboard_note_translate(
    text: str, target_locale: str, source_locale: str | None = None
) -> TranslationResponse:
    translator = deepl_translator()
    result = translator.translate_text(
        text,
        target_lang=target_locale.upper(),
        source_lang=source_locale.upper() if source_locale else None,
    )
    detected_source = getattr(result, "detected_source_lang", None)
    return TranslationResponse(
        translated_text=result.text,
        target_locale=target_locale,
        detected_source_locale=detected_source,
    )
