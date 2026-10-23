import os
from typing import Optional

from google.cloud import translate_v2 as translate

from vision_models import (
    TranslationRequest,
    TranslationResponse,
)


GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
DEFAULT_TARGET_LANGUAGE = os.environ.get("TRANSLATE_TARGET_LANGUAGE", "es")


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = translate.Client()

    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language
        if request.source_language != "auto"
        else None,
        format_="text",
    )

    translated = result.get("translatedText", "")
    detected_source = result.get("detectedSourceLanguage", request.source_language)

    return TranslationResponse(
        translated_text=translated,
        source_language=detected_source,
        target_language=request.target_language,
        model="google-translate",
    )


def translate_alt_text(
    alt_text: str,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: str = "en",
) -> TranslationResponse:
    request = TranslationRequest(
        text=alt_text,
        source_language=source_language,
        target_language=target_language,
    )
    return translate_text(request)


def translate_multiple_alt_texts(
    alt_texts: list,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: str = "en",
) -> list:
    client = translate.Client()

    results = client.translate(
        alt_texts,
        target_language=target_language,
        source_language=source_language if source_language != "auto" else None,
        format_="text",
    )

    translations = []
    for i, result in enumerate(results):
        translations.append(
            TranslationResponse(
                translated_text=result.get("translatedText", alt_texts[i]),
                source_language=result.get("detectedSourceLanguage", source_language),
                target_language=target_language,
                model="google-translate",
            )
        )

    return translations
