from __future__ import annotations

from deepl import DeepLClient


DEEPL_API_HOST = "api.deepl.com"


def alt_text_translate(description: str, target_lang: str, auth_key: str) -> str:
    client = DeepLClient(auth_key)
    result = client.translate_text(description, target_lang=target_lang)
    return result.text.strip()
