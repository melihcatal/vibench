# Translates a single text string between languages using DeepL API
from typing import Optional
from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = TranslationClient()
    source_lang, target_lang = client.normalize_languages(
        request.get("source_lang"), request["target_lang"]
    )

    result = client.client.translate_text(
        request["text"],
        source_lang=source_lang,
        target_lang=target_lang
    )

    return TranslationResponse(
        translated_text=result.text,
        detected_source_lang=result.detected_source_lang,
        model="DeepL"
    )