import os
from google.cloud import translate_v2 as translate
from safety_models import AppealRequest, TranslatedAppeal

def translate_appeal_text(request: AppealRequest, target_language: str = "en") -> TranslatedAppeal:
    """
    Translates appeal text for review using Google Cloud Translation.
    """
    # Google Cloud Translation client setup
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    translate_client = translate.Client()

    # Detect source language
    detection = translate_client.detect_language(request.appeal_reason)
    source_language = detection['language']

    # Translate the text
    result = translate_client.translate(
        request.appeal_reason,
        target_language=target_language,
        source_language=source_language
    )

    return TranslatedAppeal(
        translated_text=result['translatedText'],
        source_language=source_language,
        target_language=target_language
    )
