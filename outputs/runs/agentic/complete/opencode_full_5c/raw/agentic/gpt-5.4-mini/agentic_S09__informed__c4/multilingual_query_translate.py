import os

from deepl import DeepLClient


def translate_query(query: str, target_language: str = "en") -> str:
    client = DeepLClient(os.getenv("DEEPL_AUTH_KEY", ""))
    result = client.translate_text(query, target_lang=target_language.upper())
    return result.text
