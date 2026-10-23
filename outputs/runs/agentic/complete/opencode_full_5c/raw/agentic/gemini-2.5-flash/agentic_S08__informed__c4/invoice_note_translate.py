import os
from document_client import get_google_translate_client


def translate_invoice_notes(text_to_translate: str, target_language: str = "en") -> str:
    client = get_google_translate_client()

    # The GOOGLE_APPLICATION_CREDENTIALS environment variable needs to be set
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    result = client.translate(text_to_translate, target_language=target_language)
    return result["translatedText"]
