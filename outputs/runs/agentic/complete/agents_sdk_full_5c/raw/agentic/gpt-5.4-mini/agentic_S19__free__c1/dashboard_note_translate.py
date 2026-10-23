from __future__ import annotations

from typing import Any, Dict

from google.cloud import translate_v3


def dashboard_note_translate(text: str, target_locale: str) -> Dict[str, Any]:
    client = translate_v3.TranslationServiceClient()
    parent = client.common_location_path("my-project", "global")
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_locale,
        }
    )
    translated = response.translations[0].translated_text if response.translations else text
    return {"source_text": text, "translated_text": translated, "target_locale": target_locale, "provider": "google-cloud-translate"}
