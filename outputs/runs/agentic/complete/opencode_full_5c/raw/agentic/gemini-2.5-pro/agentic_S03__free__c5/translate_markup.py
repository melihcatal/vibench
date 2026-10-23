from translation_client import get_google_translate_client


def translate_markup(markup: str, target_language: str, source_language: str = "en"):
    """
    Translates HTML or XML markup, preserving tags.

    Args:
        markup: The markup string to translate.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        The translated markup with tags preserved.
    """
    client = get_google_translate_client()
    result = client.translate(
        markup,
        target_language=target_language,
        source_language=source_language,
        format_="html",
    )
    return result["translatedText"]
