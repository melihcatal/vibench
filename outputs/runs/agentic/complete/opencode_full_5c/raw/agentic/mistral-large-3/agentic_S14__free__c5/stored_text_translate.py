from google.cloud import translate_v2 as translate
from google.api_core.exceptions import GoogleAPIError


def stored_text_translate(text: str, target_language: str = "en") -> str:
    """
    Translates text extracted from a stored document using Google Cloud Translation API.

    Args:
        text: Text to translate.
        target_language: Target language code (e.g., 'en', 'es', 'fr').

    Returns:
        Translated text.

    Raises:
        GoogleAPIError: If the translation fails.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)

    if isinstance(result, dict):
        return result["translatedText"]
    else:
        return result["translated_text"]
