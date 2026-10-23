from __future__ import annotations

from google.cloud import translate_v3


def dashboard_note_translate(text: str, target_locale: str) -> dict:
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path(project="", location="global")
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_locale,
        }
    )
    translated = response.translations[0].translated_text if response.translations else text
    return {"translated_text": translated, "provider": "google.cloud.translate_v3"}
