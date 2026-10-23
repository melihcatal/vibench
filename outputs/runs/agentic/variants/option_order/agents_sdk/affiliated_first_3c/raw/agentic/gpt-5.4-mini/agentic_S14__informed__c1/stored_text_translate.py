from __future__ import annotations

from typing import Optional

from google.cloud import translate_v3 as translate

from storage_models import NormalizedText


def translate_stored_text(text: str, target_language: str, project_id: str, location: str = "global") -> NormalizedText:
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    translated = response.translations[0].translated_text if response.translations else ""
    return NormalizedText(text=translated, language=target_language, source="google-cloud-translation")
