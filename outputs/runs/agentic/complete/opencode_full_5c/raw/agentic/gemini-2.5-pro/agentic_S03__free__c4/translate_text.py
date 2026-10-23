from translation_client import get_translation_client


def translate_text(text: str, target_language: str, source_language: str = None):
    """
    Translates a single text string.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into.
        source_language: The source language of the text. If None, the API will
                         attempt to detect the source language.

    Returns:
        A dictionary containing the translated text and detected source language.
    """
    client = get_translation_client()
    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language if source_language else "",
    )
    return result
