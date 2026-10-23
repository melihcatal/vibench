from __future__ import annotations

from typing import Optional

from speech_client import GoogleSpeechClient
from speech_models import TranslationResult


def translate_script(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResult:
    client = GoogleSpeechClient()
    response = client.translate(text, target_language=target_language, source_language=source_language)
    translated = response.get("data", {}).get("translations", [{}])[0].get("translatedText", "")
    return TranslationResult(
        translated_text=translated,
        target_language=target_language,
        raw_response=response,
    )
