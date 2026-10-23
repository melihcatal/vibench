import os
from google.cloud import translate_v3 as translate
from vision_models import ImageDescriptionResult

def translate_image_description(description: ImageDescriptionResult, target_language_code: str = "es") -> str:
    """
    Translates generated image descriptions using Google Cloud Translation API.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()
    location = "global" # Translation API is global

    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [description.description],
            "target_language_code": target_language_code,
            "mime_type": "text/plain",
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text
    return translated_text
