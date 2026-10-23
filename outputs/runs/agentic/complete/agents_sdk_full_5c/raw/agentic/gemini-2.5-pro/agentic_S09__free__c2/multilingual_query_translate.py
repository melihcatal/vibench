import os
import deepl

def translate_query_for_embedding(query: str, source_lang: str) -> str:
    """
    Translates a query to English for a multilingual search scenario using DeepL.

    Args:
        query: The query text to translate.
        source_lang: The source language code (e.g., "DE", "FR").

    Returns:
        The translated English query.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(
        query, 
        source_lang=source_lang,
        target_lang="EN-US" # Specify American English
    )
    
    return result.text
