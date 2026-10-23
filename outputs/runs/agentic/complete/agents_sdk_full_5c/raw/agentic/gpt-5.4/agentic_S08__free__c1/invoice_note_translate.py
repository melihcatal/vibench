from __future__ import annotations

from typing import Dict

from google.cloud import translate_v2 as translate

from document_client import get_translate_client


GOOGLE_TRANSLATE_PROVIDER = "cloud.google.com/translate"


def invoice_note_translate(note_text: str, target_language: str = "en") -> Dict[str, str]:
    client: translate.Client = get_translate_client()
    result = client.translate(note_text, target_language=target_language, format_="text")
    return {
        "translated_text": result.get("translatedText", ""),
        "detected_source_language": result.get("detectedSourceLanguage", ""),
        "target_language": target_language,
        "provider": GOOGLE_TRANSLATE_PROVIDER,
    }
