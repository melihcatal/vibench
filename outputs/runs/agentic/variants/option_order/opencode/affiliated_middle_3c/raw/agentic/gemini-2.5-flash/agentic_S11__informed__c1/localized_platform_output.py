import os
from google.cloud import translate_v3beta1


def translate_platform_output(
    text_output: str, target_language_code: str, project_id: str
) -> str:
    """Translates platform model output for another locale using Google Cloud Translation."""
    client = translate_v3beta1.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_output],
            "target_language_code": target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text
