import os
from google.cloud import translate_v3 as translate


def translate_text(text: str, target_language_code: str, project_id: str) -> str:
    """
    Translates user-facing document fields using Google Cloud Translation.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    client = translate.TranslationServiceClient()

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

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
