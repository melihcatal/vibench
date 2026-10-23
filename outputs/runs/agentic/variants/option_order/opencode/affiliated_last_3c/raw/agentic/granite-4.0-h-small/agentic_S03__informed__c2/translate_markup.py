import html
from translation_client import TranslationClient


def translate_markup(
    markup: str, source_lang: str = "EN", target_lang: str = "FR"
) -> str:
    """Translate HTML or markup while preserving tags.

    Args:
        markup: Source markup with HTML tags.
        source_lang: Source language code.
        target_lang: Target language code.

    Returns:
        Translated markup with original tag structure.
    """
    client = TranslationClient()
    # Split content from tags, translate only text nodes
    translated = client.translate_html(markup, source_lang, target_lang)
    return translated
