from google.cloud import translate_v3 as translate
import os

def translate_text(text: str, target_language: str = "es", project_id: str | None = None) -> str:
    if not project_id:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set or project_id not provided.")

    client = translate.TranslationServiceClient()

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
