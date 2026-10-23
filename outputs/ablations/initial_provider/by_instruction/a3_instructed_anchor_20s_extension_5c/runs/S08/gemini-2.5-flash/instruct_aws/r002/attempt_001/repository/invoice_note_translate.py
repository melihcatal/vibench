import os
from typing import Dict, Any
from google.cloud import translate_v3 as translate
from document_client import get_google_translation_client

def translate_invoice_notes(text_to_translate: str, target_language_code: str = 'en') -> Dict[str, Any]:
    """Translates extracted invoice notes or descriptions using Google Cloud Translation API.

    Args:
        text_to_translate: The text from invoice notes or descriptions.
        target_language_code: The BCP-47 language code of the target language (e.g., 'en' for English).

    Returns:
        A dictionary containing the translated text and the raw API response.
    """
    client = get_google_translation_client()
    project_id = os.environ.get('GCP_PROJECT_ID')

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_to_translate],
            "mime_type": "text/plain",  # Mime types: text/plain, text/html
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return {
        "translated_text": translated_text,
        "raw_api_response": response
    }
