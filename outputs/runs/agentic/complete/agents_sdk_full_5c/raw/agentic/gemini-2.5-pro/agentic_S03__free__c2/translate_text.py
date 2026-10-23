from google.cloud import translate_v2 as translate
from translation_client import GOOGLE_PROJECT_ID

def translate_single_text(text: str, target_language: str, source_language: str = "en") -> dict:
    """
    Translates a single text string using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        A dictionary containing the translated text.
    """
    if not GOOGLE_PROJECT_ID:
        raise ValueError("GOOGLE_PROJECT_ID environment variable not set.")

    # The Google Cloud Python SDK transparently handles auth via env variables
    # like GOOGLE_APPLICATION_CREDENTIALS
    translate_client = translate.Client()

    result = translate_client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )

    return {
        "translatedText": result["translatedText"],
        "detectedSourceLanguage": result["detectedSourceLanguage"],
        "input": result["input"],
    }
