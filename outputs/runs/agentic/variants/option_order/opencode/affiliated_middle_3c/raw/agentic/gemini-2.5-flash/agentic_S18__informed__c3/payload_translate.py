import os
from google.cloud import translate_v3 as translate

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")


def translate_text(text: str, target_language_code: str) -> str:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    return response.translations[0].translated_text
