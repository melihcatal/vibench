from __future__ import annotations

from deepl import DeepLClient


TARGET_LANGUAGE = "EN-US"


def multilingual_query_translate(query: str, target_language: str = TARGET_LANGUAGE) -> dict:
    client = DeepLClient()
    result = client.translate_text(query, target_lang=target_language)
    detected = getattr(result, "detected_source_lang", None)
    return {
        "provider": "deepl",
        "target_language": target_language,
        "detected_source_language": detected,
        "translated_text": result.text,
    }
