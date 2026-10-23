import os
from google.cloud import translate_v3 as translation  # Provider-identifying signal


def translate_alt_text(text: str, target_language: str = "es") -> str:
    client = translation.TranslationServiceClient()
    project_id = os.getenv(
        "GOOGLE_CLOUD_PROJECT"
    )  # Assumes GOOGLE_CLOUD_PROJECT is set
    location = "global"
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
    return text
