from google.cloud import translate_v3 as translate  # Google Cloud Translation API
import os


def translate_text_field(text: str, target_language: str, project_id: str) -> str:
    """
    Translates user-facing document fields using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()

    location = "global"  # Google Cloud Translation API location
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text
