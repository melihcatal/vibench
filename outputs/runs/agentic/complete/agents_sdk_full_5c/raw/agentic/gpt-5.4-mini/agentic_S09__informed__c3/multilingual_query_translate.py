from deepl import Translator
import os


def multilingual_query_translate(query: str, target_language: str = "EN-US") -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required for DeepL API")
    translator = Translator(auth_key)
    result = translator.translate_text(query, target_lang=target_language)
    return result.text
