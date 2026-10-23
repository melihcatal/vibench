from google.cloud import translate_v2 as translate
import os

from translation_client import get_google_project_id

def translate_text(
    text: str, target_language: str, source_language: str = "en"
) -> str:
    """Translates a single text string using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        The translated text.
    """
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise EnvironmentError(
            "Google Cloud credentials not found. Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable."
        )

    translate_client = translate.Client()

    result = translate_client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]
