# Translates a list of strings while preserving order using DeepL API
from typing import List
from translation_client import TranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse, TranslationResponse


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = TranslationClient()
    source_lang, target_lang = client.normalize_languages(
        request.get("source_lang"), request["target_lang"]
    )

    results = client.client.translate_text(
        request["texts"],
        source_lang=source_lang,
        target_lang=target_lang
    )

    translations = [
        TranslationResponse(
            translated_text=result.text,
            detected_source_lang=result.detected_source_lang,
            model="DeepL"
        )
        for result in results
    ]

    return BatchTranslationResponse(translations=translations, model="DeepL")