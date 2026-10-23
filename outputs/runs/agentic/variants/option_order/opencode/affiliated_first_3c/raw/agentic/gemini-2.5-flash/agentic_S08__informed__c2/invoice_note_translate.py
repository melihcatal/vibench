import os
from google.cloud import translate_v3 as translate


def translate_invoice_note(
    text: str, target_language_code: str, project_id: str
) -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set.
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text
