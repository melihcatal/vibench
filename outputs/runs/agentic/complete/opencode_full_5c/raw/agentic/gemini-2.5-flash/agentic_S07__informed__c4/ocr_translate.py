import os
from google.cloud import translate_v3 as translate


def translate_text(
    text: str, target_language: str = "es", project_id: str = None
) -> str:
    """
    Translates extracted OCR text using Google Cloud Translation.
    """
    client = translate.TranslationServiceClient()

    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError(
            "Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT env var not set."
        )

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text
