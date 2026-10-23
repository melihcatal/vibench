import deepl
from translation_client import TranslationClient


def batch_translate(
    texts: list[str], source_lang: str = "EN", target_lang: str = "FR"
) -> list[str]:
    """Translate a list of strings while preserving order.

    Args:
        texts: List of source texts.
        source_lang: Source language (default EN).
        target_lang: Target language (default FR).

    Returns:
        List of translated texts in same order.
    """
    client = TranslationClient()
    results = client.translate_batch(texts, source_lang, target_lang)
    return [r.translated_text for r in results]
