from google.cloud import translate
import os


def record_translate(text_content: str, target_language: str) -> str:
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "target_language_code": target_language,
        }
    )

    return response.translations[0].translated_text
