from translation_client import get_translation_client


def translate_text(text: str, target_language: str, source_language: str = "en"):
    """
    Translates a single text string to a target language.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        The translated text string.
    """
    client = get_translation_client()
    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )
    return result["translatedText"]
