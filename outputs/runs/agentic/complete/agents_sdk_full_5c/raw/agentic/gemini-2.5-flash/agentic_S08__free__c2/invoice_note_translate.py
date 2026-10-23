import os
from typing import Optional
from google.cloud import translate_v3 as translate
from document_client import DocumentClients, PROJECT_ID, LOCATION

def translate_invoice_note(text: str, target_language_code: str = "en", source_language_code: Optional[str] = None) -> str:
    """Translates extracted invoice notes or descriptions using Google Cloud Translation API.

    Args:
        text: The text content to translate.
        target_language_code: The BCP-47 language code of the target language.
        source_language_code: Optional. The BCP-47 language code of the source language.
                              If not specified, the API will attempt to detect the source language.

    Returns:
        The translated text.
    """
    client = DocumentClients.get_translate_client()

    parent = f"projects/{PROJECT_ID}/locations/{LOCATION}"

    if source_language_code:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
                "source_language_code": source_language_code,
            }
        )
    else:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text
