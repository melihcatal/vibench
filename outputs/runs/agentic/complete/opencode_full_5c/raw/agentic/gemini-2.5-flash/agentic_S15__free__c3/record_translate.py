import os
from google.cloud import translate_v3 as translate


def translate_document_field(
    text_content: str, target_language: str, project_id: str, location: str = "global"
) -> str:
    """
    Translates user-facing document fields using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "target_language_code": target_language,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text_content
