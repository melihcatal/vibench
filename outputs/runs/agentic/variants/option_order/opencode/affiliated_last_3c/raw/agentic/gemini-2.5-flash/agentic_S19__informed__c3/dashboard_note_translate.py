import os
from google.cloud import translate


def translate_dashboard_note(
    text: str, target_language_code: str, project_id: str
) -> str:
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text
