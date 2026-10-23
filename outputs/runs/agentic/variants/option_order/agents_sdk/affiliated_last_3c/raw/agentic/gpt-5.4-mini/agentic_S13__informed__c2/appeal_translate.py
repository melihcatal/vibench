from __future__ import annotations

from google.cloud import translate_v3 as translate

PROJECT_ID_ENV = "GOOGLE_CLOUD_PROJECT"
LOCATION = "global"
TARGET_LANGUAGE = "en"


def appeal_translate(text: str, source_language: str) -> str:
    client = translate.TranslationServiceClient()
    project_id = __import__("os").environ[PROJECT_ID_ENV]
    parent = f"projects/{project_id}/locations/{LOCATION}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": TARGET_LANGUAGE,
        }
    )
    return response.translations[0].translated_text if response.translations else ""
