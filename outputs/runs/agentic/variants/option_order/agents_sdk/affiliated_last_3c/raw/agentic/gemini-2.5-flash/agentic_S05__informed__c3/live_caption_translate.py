from google.cloud import translate_v3beta1 as translate
import os

def translate_caption(text: str, target_language: str = "es") -> str:
    """Translates live captions into another language using Google Cloud Translation."""
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") # Or specify directly
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
            "mime_type": "text/plain",
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return text
