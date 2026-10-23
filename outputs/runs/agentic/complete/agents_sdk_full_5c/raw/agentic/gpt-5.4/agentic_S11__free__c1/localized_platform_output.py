from __future__ import annotations

from deepl import DeepLClient


DEEPL_API_URL = "https://api.deepl.com"



def localized_platform_output(text: str, target_lang: str) -> dict:
    auth_key = __import__("os").environ["DEEPL_AUTH_KEY"]
    client = DeepLClient(auth_key)
    response = client.translate_text(text, target_lang=target_lang)
    return {
        "translated_text": response.text,
        "detected_source_lang": response.detected_source_lang,
        "target_lang": target_lang,
        "provider": "DeepL",
        "provider_response": response,
    }
