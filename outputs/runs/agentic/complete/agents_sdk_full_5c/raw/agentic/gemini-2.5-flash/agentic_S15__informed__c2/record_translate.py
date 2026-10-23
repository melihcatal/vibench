import os
from google.cloud import translate_v2 as translate

def translate_text_fields(text_content: str, target_language: str = "es") -> str:
    """Translates user-facing document fields using Google Cloud Translation.

    Args:
        text_content: The string content to translate.
        target_language: The target language code (e.g., 'es' for Spanish, 'fr' for French).

    Returns:
        The translated text content.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # for authentication.
    translate_client = translate.Client()

    result = translate_client.translate(text_content, target_language=target_language)

    # The translated text is in result['translatedText']
    return result['translatedText']
