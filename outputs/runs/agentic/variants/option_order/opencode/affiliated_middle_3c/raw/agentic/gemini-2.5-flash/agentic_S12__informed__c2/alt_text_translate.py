import os
from google.cloud import translate


def translate_alt_text(text: str, target_language: str = "en") -> str:
    client = translate.TranslationServiceClient()

    # Google Cloud project ID from environment variable or default configuration
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
