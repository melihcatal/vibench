from translation_client import get_translation_client


def translate_text(text: str, target_language: str, source_language: str = "en") -> str:
    """
    Translates a single text string to a target language.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., 'fr', 'de').
        source_language: The source language code (e.g., 'en').

    Returns:
        The translated text.
    """
    client = get_translation_client()
    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )
    return result["translatedText"]
