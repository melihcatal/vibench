import os
from typing import List, Dict, Any


def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translate text using DeepL API.
    Requires DEEPL_AUTH_KEY environment variable.
    """
    import deepl

    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)
    return result.text


def multilingual_query_translate(
    queries: List[str], target_language: str = "en"
) -> Dict[str, Any]:
    """
    Translate a list of queries for multilingual embedding search using DeepL API.
    """
    translated = []
    for query in queries:
        try:
            translated.append(translate_text(query, target_language))
        except Exception as e:
            translated.append(f"Translation error: {str(e)}")

    return {
        "original_queries": queries,
        "translated_queries": translated,
        "target_language": target_language,
    }
