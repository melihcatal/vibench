import os
from google.cloud import translate_v3 as translate


def translate_log_message(
    text: str, target_language: str, project_id: str = None
) -> str:
    client = translate.TranslationServiceClient()

    if not project_id:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "Google Cloud Project ID not found. Set GOOGLE_CLOUD_PROJECT environment variable or pass project_id."
            )

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
