import os
from google.cloud import translate_v3 as translate


def translate_live_caption(
    text: str, target_language_code: str, project_id: str
) -> str:
    """
    Translates a live caption into another language using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    client = translate.TranslationServiceClient()

    # Provider-identifying signal: google.cloud.translate_v3
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
