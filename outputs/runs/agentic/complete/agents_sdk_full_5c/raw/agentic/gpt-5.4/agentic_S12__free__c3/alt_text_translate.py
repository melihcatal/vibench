from __future__ import annotations

from vision_client import DEEPL_TARGET_LANG, get_deepl_client
from vision_models import TranslationResult


def alt_text_translate(description: str, target_language: str = DEEPL_TARGET_LANG) -> TranslationResult:
    client = get_deepl_client()
    response = client.translate_text(description, target_lang=target_language)
    return TranslationResult(
        translated_text=response.text,
        target_language=target_language,
        raw_response={"detected_source_language": response.detected_source_lang, "billed_characters": response.billed_characters},
    )
