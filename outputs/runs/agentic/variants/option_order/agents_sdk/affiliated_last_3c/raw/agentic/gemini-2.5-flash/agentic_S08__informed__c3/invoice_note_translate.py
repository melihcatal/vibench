import os
from google.cloud import translate_v3 as translate
from document_client import get_google_translate_config

def translate_invoice_notes(text: str, target_language_code: str = "en") -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.
    """
    config = get_google_translate_config()
    project_id = config["project_id"]

    client = translate.TranslationServiceClient()

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

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text
