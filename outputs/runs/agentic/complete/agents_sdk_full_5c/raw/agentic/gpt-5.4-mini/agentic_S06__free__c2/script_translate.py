from __future__ import annotations

from google.cloud import translate_v3


def translate_script(text: str, target_language_code: str, project_id: str, location: str = "global") -> str:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )
    return response.translations[0].translated_text if response.translations else text
