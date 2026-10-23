
from google.cloud import translate_v2 as translate

def translate_consent_copy(text: str, target_language: str) -> str:
    """
    Translates identity-provider consent copy using Google Cloud Translation API.

    Args:
        text: The consent copy to translate.
        target_language: The target language for the translation (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
