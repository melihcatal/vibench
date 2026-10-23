import deepl
from translation_client import TranslationClient


def translate_text(text: str, source_lang: str = "EN", target_lang: str = "FR") -> str:
    """Translate a single text string using DeepL API.

    Args:
        text: The source text to translate.
        source_lang: Source language code (default EN).
        target_lang: Target language code (default FR).

    Returns:
        Translated text.
    """
    client = TranslationClient()
    result = client.translate(text, source_lang, target_lang)
    return result.translated_text
