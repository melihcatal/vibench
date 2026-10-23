import os
from typing import Optional
from google.cloud import translate_v3 as translate
from document_client import get_translate_client

def translate_invoice_note(text: str, target_language_code: str, project_id: str) -> Optional[str]:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation API.
    """
    if not text:
        return None

    client = get_translate_client()
    parent = f"projects/{project_id}/locations/global"

    try:
        response = client.translate_text(
            parent=parent,
            contents=[text],
            target_language_code=target_language_code,
            model=f"projects/{project_id}/locations/global/models/general/nmt"
        )
        if response.translations:
            return response.translations[0].translated_text
        return None
    except Exception as e:
        print(f"Error during translation with Google Cloud Translate: {e}")
        return None
