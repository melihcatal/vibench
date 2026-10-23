import os
from google.cloud import translate_v2 as translate
from identity_models import TranslationRequest, TranslationResponse


def translate_welcome_text(
    text: str, target_language: str, source_language: str = None
) -> TranslationResponse:
    """
    Translate onboarding copy into the user's locale using Google Cloud Translation API.
    """
    # Initialize Google Cloud Translation client
    client = translate.Client()

    # Translate the text
    if source_language:
        result = client.translate(
            text, target_language=target_language, source_language=source_language
        )
    else:
        result = client.translate(text, target_language=target_language)

    return TranslationResponse(
        translated_text=result["translatedText"],
        source_language=result.get("detectedSourceLanguage", source_language or "en"),
        target_language=target_language,
    )
