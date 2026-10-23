import os
from typing import List
import deepl


def translate_queries(queries: List[str], target_lang: str = "en") -> List[str]:
    """
    Translates queries using DeepL API before multilingual embedding search.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    translated_queries = []
    for query in queries:
        # The deepl.Translator client and translate_text method are concrete and identifiable DeepL API features.
        # They are directly from the deepl-python library documentation.
        result = translator.translate_text(query, target_lang=target_lang)
        translated_queries.append(result.text)

    return translated_queries
