from google.cloud import translate_v3 as translate
import os

def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation API.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "global" # Global endpoint for general translation

    if not project_id:
        return "Error: GOOGLE_CLOUD_PROJECT environment variable not set for Translation API."

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
            "mime_type": "text/plain",  # or "text/html"
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text
