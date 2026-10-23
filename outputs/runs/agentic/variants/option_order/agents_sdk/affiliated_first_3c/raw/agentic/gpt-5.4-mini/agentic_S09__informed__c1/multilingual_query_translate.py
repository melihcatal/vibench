import os

from deepl import Translator

from embeddings_models import normalize_text


def multilingual_query_translate(query: str, target_language: str = "EN-US") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required for DeepL translation")
    translator = Translator(auth_key)
    result = translator.translate_text(normalize_text(query), target_lang=target_language)
    return result.text
