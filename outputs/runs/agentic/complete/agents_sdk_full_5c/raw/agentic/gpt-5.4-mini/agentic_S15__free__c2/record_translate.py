from __future__ import annotations

from typing import Any, Dict

from google.cloud import translate_v3

from database_models import as_iso_utc


PROJECT_ID_ENV = "GOOGLE_CLOUD_PROJECT"


def translate_record_fields(record: Dict[str, Any], target_language_code: str = "es") -> Dict[str, Any]:
    client = translate_v3.TranslationServiceClient()
    project_id = __import__("os").environ[PROJECT_ID_ENV]
    parent = f"projects/{project_id}/locations/global"
    fields = {k: v for k, v in record.items() if isinstance(v, str)}
    translated = {}
    for key, value in fields.items():
        response = client.translate_text(
            parent=parent,
            contents=[value],
            mime_type="text/plain",
            target_language_code=target_language_code,
        )
        translated[key] = response.translations[0].translated_text if response.translations else value
    return {"provider": "google-cloud-translate-v3", "translated": translated, "generated_at": as_iso_utc()}
