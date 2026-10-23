import os
from google.cloud import translate


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    client = translate.TranslationServiceClient()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    location = os.getenv(
        "GOOGLE_CLOUD_LOCATION", "global"
    )  # Translation API is often global or regional

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
