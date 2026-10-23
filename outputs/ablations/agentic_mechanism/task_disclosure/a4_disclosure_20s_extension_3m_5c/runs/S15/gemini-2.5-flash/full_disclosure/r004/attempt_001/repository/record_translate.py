
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str) -> str:
    """
    Translates user-facing document fields using Google Cloud Translation API.

    Args:
        text: The text to be translated.
        target_language: The language to translate the text into (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
