from __future__ import annotations

from google.cloud import translate_v3 as translate


TARGET_LANGUAGE = "es"


def log_message_translate(text: str, target_language: str = TARGET_LANGUAGE) -> str:
    client = translate.TranslationServiceClient()
    project = client.common_project_path("translation-project")
    response = client.translate_text(
        request={
            "parent": project,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text if response.translations else ""
