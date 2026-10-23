import os
from deep_translator import GoogleTranslator


def translate_query(query: str, target_lang: str = "en") -> str:
    """Translate a query into the target language using Google Cloud Translation.

    Args:
        query (str): The original query text.
        target_lang (str): ISO language code for the destination language (default: "en").

    Returns:
        str: The translated query.
    """
    translator = GoogleTranslator(source="auto", target=target_lang)
    translated = translator.translate(query)
    return translated
