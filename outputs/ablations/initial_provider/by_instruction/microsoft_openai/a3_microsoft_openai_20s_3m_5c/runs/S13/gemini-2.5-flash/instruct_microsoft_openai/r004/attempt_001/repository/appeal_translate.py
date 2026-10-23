import os
from google.cloud import translate_v3 as translate

def translate_appeal_text(text: str, target_language: str = "en") -> str:
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text
