import os
from google.cloud import translate_v3 as translate


def translate_narration_script(
    text: str, target_language_code: str, project_id: str
) -> str:
    """
    Translates narration scripts using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}"

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
