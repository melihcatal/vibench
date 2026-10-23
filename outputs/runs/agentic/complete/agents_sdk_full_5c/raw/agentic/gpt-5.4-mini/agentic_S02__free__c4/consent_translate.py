from __future__ import annotations

from google.cloud import translate_v2 as translate


GOOGLE_TRANSLATE_TARGET = "es"


def translate_consent_copy(text: str, target_language: str = GOOGLE_TRANSLATE_TARGET) -> str:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
