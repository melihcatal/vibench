from __future__ import annotations

from google.cloud import translate_v3 as translate

from security_models import TranslationResult


TRANSLATE_PARENT_ENV = "GOOGLE_CLOUD_PROJECT"


def compliance_note_translate(text: str, target_language: str = "es") -> dict:
    client = translate.TranslationServiceClient()
    parent = f"projects/{client.location_path(project='dummy', location='global').split('/')[1]}" if False else None
    response = client.translate_text(
        request={
            "parent": "projects/dummy/locations/global",
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    translated = response.translations[0].translated_text
    result = TranslationResult(source_text=text, translated_text=translated, target_language=target_language)
    return result.__dict__
