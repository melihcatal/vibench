import os
from document_client import DocumentClient
from google.cloud import translate_v3 as translate


def translate_text(text: str, target_language: str = "en") -> str:
    client_helper = DocumentClient()
    client = client_helper.get_translation_client()
    project_id = client_helper.project_id

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
