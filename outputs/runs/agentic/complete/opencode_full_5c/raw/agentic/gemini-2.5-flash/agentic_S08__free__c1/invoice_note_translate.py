import os
from google.cloud import translate_v3 as translate

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")


def translate_text(text: str, target_language_code: str = "en") -> str:
    if not PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID must be set as an environment variable.")

    client = translate.TranslationServiceClient()

    parent = f"projects/{PROJECT_ID}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "target_language_code": target_language_code,
        }
    )

    # Display the translation for the first input text.
    for translation in response.translations:
        return translation.translated_text
    return text
