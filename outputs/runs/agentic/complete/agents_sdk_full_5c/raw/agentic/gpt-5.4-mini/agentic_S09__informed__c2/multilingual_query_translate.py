import os

from deep_translator import DeeplTranslator


DEEPL_PROVIDER = "DeepL API"


def translate_query(query: str, target_language: str = "en") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = DeeplTranslator(api_key=auth_key, source="auto", target=target_language)
    return translator.translate(query)
