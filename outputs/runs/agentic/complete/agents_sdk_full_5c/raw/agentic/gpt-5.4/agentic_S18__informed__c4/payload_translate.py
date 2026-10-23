from __future__ import annotations

from typing import Any, Dict

from messaging_client import get_translate_client


PROVIDER = "amazon_translate"


def translate_payload_text(text: str, source_language: str, target_language: str) -> Dict[str, Any]:
    client = get_translate_client()
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return {
        "provider": PROVIDER,
        "translated_text": response["TranslatedText"],
        "source_language": response.get("SourceLanguageCode", source_language),
        "target_language": response.get("TargetLanguageCode", target_language),
    }
