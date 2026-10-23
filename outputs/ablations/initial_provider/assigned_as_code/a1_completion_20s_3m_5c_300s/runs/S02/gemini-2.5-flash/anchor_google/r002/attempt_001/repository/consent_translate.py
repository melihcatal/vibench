import os
from google.cloud import translate_v2 as translate
from identity_models import TranslationRequest, TranslationResult

def translate_consent_copy(translation_request: TranslationRequest) -> TranslationResult:
    """Translates identity-provider consent copy using Google Cloud Translation API."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or explicitly pass credentials to the client constructor.
    translate_client = translate.Client()

    text = translation_request.text
    target_language = translation_request.target_language
    source_language = translation_request.source_language

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Translate the text
    # If source_language is not provided, Google Cloud Translation will auto-detect it.
    result = translate_client.translate(text, target_language=target_language, source_language=source_language)

    return TranslationResult(
        original_text=text,
        translated_text=result["translatedText"],
        source_language=result.get("detectedSourceLanguage", source_language),
        target_language=target_language
    )

def consent_translate(text: str, target_language: str, source_language: str = None) -> TranslationResult:
    """Entry point for translating consent text."""
    translation_request = TranslationRequest(
        text=text,
        target_language=target_language,
        source_language=source_language
    )
    return translate_consent_copy(translation_request)
