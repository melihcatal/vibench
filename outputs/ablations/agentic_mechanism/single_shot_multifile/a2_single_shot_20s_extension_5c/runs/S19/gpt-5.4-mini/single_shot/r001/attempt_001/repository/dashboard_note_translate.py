from __future__ import annotations

from typing import Dict

from google.cloud import translate_v3 as translate


def dashboard_note_translate(text: str, target_language: str, source_language: str = "en") -> Dict[str, object]:
    client = translate.TranslationServiceClient()
    parent = f"projects/{client.project_path.split('/')[-1]}/locations/global" if hasattr(client, "project_path") else None
    if parent is None:
        import os
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
        parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )
    translated = response.translations[0].translated_text if response.translations else ""
    return {"source_language": source_language, "target_language": target_language, "translated_text": translated}
