from storage_client import get_translate_client
from storage_models import TranslatedText


def translate_text(text: str, target_language: str = "en") -> TranslatedText:
    """
    Translates text using the Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language.

    Returns:
        A TranslatedText object with the original, translated text, and target language.
    """
    translate_client = get_translate_client()

    result = translate_client.translate(text, target_language=target_language)

    return TranslatedText(
        source_text=text,
        translated_text=result["translatedText"],
        target_language=target_language,
    )
