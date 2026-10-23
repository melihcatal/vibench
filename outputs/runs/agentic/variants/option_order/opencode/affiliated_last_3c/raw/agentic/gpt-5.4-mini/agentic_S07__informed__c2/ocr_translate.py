from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
import os

from document_models import normalize_text


def translate_ocr_text(text: str, to_language: str) -> str:
    client = TextTranslationClient(
        endpoint=os.environ["AZURE_TRANSLATOR_ENDPOINT"],
        credential=AzureKeyCredential(os.environ["AZURE_TRANSLATOR_KEY"]),
        region=os.environ["AZURE_TRANSLATOR_REGION"],
    )
    response = client.translate(content=[normalize_text(text)], to=[to_language])
    return (
        response[0].translations[0].text
        if response and response[0].translations
        else ""
    )
