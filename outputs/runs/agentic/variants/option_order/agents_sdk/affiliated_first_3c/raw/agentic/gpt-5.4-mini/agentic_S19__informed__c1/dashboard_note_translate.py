from __future__ import annotations

from typing import Dict

from google.cloud import translate_v3 as translate


def dashboard_note_translate(text: str, target_language: str, project_id: str, location: str = "global") -> Dict[str, str]:
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent, mime_type="text/plain")
    translated = response.translations[0].translated_text if response.translations else ""
    return {"source_text": text, "translated_text": translated, "target_language": target_language, "provider": "Cloud Translation"}
