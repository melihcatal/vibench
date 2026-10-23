import os
from google.cloud import translate


def translate_dashboard_note(
    text: str,
    target_language_code: str,
    project_id: str,
) -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )

    # Assuming only one text is translated
    return response.translations[0].translated_text
