from translation_client import get_translation_client


def translate_markup(markup: str, target_language: str, source_language: str = "en"):
    """
    Translates HTML or markup, preserving tags, using Google Cloud Translation.
    """
    client = get_translation_client()
    result = client.translate(
        markup,
        target_language=target_language,
        source_language=source_language,
        format_="html",
    )
    return result["translatedText"]
