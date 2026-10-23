
import os
from document_client import get_azure_translator_client

def translate_text(text: str, target_language: str = "en") -> str:
    client = get_azure_translator_client()

    response = client.translate_to(
        body=[{"text": text}],
        to=[target_language]
    )

    if response and response[0].translations:
        return response[0].translations[0].text
    return text
