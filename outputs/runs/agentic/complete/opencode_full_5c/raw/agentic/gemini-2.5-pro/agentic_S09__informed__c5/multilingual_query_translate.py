from embeddings_client import get_deepl_translator


def translate_query(query: str, target_lang: str) -> str:
    """
    Translates a query to the target language using DeepL API.

    Args:
        query: The text to translate.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        The translated text.
    """
    translator = get_deepl_translator()
    result = translator.translate_text(query, target_lang=target_lang)
    return result.text
