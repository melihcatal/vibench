from __future__ import annotations

from typing import Any, Dict

from google.cloud import translate_v3 as translate


class RecordTranslator:
    def __init__(self, project_id: str | None = None, location: str = "global") -> None:
        self.client = translate.TranslationServiceClient()
        self.project_id = project_id
        self.location = location

    def translate_text(self, text: str, target_language: str, source_language: str | None = None) -> str:
        parent = f"projects/{self.project_id}/locations/{self.location}" if self.project_id else f"locations/{self.location}"
        response = self.client.translate_text(
            parent=parent,
            contents=[text],
            mime_type="text/plain",
            target_language_code=target_language,
            source_language_code=source_language or "",
        )
        return response.translations[0].translated_text if response.translations else text

    def translate_record(self, record: Dict[str, Any], target_language: str) -> Dict[str, Any]:
        translated = dict(record)
        for key, value in record.items():
            if isinstance(value, str):
                translated[key] = self.translate_text(value, target_language)
        return translated
