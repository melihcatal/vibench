import os
from google.cloud import translate

def translate_transcript_segment(text: str, target_language_code: str, project_id: str) -> str:
    """Translates a single transcript segment using Google Cloud Translation."""

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

