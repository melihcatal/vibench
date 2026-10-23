from google.cloud import translate_v3 as translate
import os
from typing import List


def translate_dashboard_note(
    text: str, target_language_code: str, project_id: str
) -> str:
    """
    Translates metric or dashboard notes for another locale using Google Cloud Translation.
    Assumes GOOGLE_APPLICATION_CREDENTIALS are set for authentication.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
    )

    if response.translations:
        return response.translations[0].translated_text
    return text
