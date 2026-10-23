from translation_client import get_translation_client


def translate_markup(
    markup: str, target_language: str, source_language: str = "en"
) -> str:
    """
    Translates HTML or other markup, preserving tags.

    Args:
        markup: The markup string to translate.
        target_language: The target language code.
        source_language: The source language code.

    Returns:
        The translated markup.
    """
    client = get_translation_client()
    result = client.translate(
        markup,
        target_language=target_language,
        source_language=source_language,
        format_="html",
    )
    return result["translatedText"]
