from __future__ import annotations

from google.cloud import translate_v3 as translate


def translate_script(text: str, target_language_code: str, project_id: str, source_language_code: str = "en") -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )
    return response.translations[0].translated_text
