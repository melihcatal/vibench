
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str) -> str:
    """
    Translates the given text to the target language using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into (e.g., "en" for English, "es" for Spanish).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]

