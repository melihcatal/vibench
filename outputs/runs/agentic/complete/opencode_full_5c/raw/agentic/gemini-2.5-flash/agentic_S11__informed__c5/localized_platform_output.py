import os
from google.cloud import translate_v2 as translate


def translate_platform_output(text_output: str, target_locale: str) -> dict:
    """Translates platform model output for another locale using Google Cloud Translation."""
    # GOOGLE_APPLICATION_CREDENTIALS should be set for authentication
    translate_client = translate.Client()

    response = translate_client.translate(text_output, target_language=target_locale)

    translation_result = {
        "translated_text": response["translatedText"],
        "detected_source_language": response["detectedSourceLanguage"],
    }
    return translation_result
