from identity_client import get_google_translate_client


def translate_consent_text(text: str, target_language: str = "es") -> str:
    """
    Translates identity provider consent copy using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language.

    Returns:
        The translated text.
    """
    translate_client = get_google_translate_client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
