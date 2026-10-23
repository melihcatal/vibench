import os
from google.cloud import translate_v3


def translate_dashboard_note(
    project_id: str, text: str, target_language: str, source_language: str = "en"
):
    client = translate_v3.TranslationServiceClient()
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

    translations = [
        translation.translated_text for translation in response.translations
    ]
    return translations[0] if translations else ""
