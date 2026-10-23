import os
from google.cloud import translate_v3 as translate

def translate_text(text: str, target_language_code: str = "es") -> str:
    """
    Translates text using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )

    # Assuming only one translation is requested and returned
    return response.translations[0].translated_text

