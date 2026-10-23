from google.cloud import translate_v3 as translate
import os


def translate_invoice_notes(
    text: str, project_id: str, target_language_code: str = "en"
) -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text
