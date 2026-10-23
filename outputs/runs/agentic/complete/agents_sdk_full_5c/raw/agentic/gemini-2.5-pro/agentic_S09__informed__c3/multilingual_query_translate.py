import os
import deepl

def translate_query_for_search(query: str, target_lang: str = "EN-US") -> str:
    """
    Translates a query into a target language using the DeepL API.

    Args:
        query: The query text to translate.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").
                     See DeepL documentation for supported languages.

    Returns:
        The translated query text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(query, target_lang=target_lang)
    
    return result.text
