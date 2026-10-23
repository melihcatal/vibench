from __future__ import annotations

from google.cloud import translate_v3


def translate_log_message(text: str, target_language: str) -> str:
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path("sample-project", "global")
    response = client.translate_text(
        contents=[text],
        target_language_code=target_language,
        parent=parent,
        mime_type="text/plain",
    )
    return response.translations[0].translated_text if response.translations else text
