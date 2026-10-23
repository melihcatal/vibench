import os
from typing import List

import deepl


def translate_queries(queries: List[str], target_lang: str = "EN-US") -> List[str]:
    """Translate queries for multilingual embedding search using DeepL."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")
    
    translator = deepl.Translator(auth_key)
    translations = []
    
    for query in queries:
        result = translator.translate_text(query, target_lang=target_lang)
        translations.append(result.text)
    
    return translations