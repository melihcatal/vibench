from __future__ import annotations

from dataclasses import dataclass

from google.cloud import translate_v3 as translate


@dataclass
class TranslationResult:
    translated_text: str
    target_language: str


def compliance_note_translate(text: str, target_language: str = "en") -> TranslationResult:
    client = translate.TranslationServiceClient()
    parent = "projects/demo-project/locations/global"
    response = client.translate_text(request={"parent": parent, "contents": [text], "mime_type": "text/plain", "target_language_code": target_language})
    return TranslationResult(translated_text=response.translations[0].translated_text if response.translations else text, target_language=target_language)
