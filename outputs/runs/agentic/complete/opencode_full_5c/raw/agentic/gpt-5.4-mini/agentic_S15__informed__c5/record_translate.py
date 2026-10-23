import os

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def record_translate(text: str, target_language: str) -> str:
    client = TextTranslationClient(
        endpoint=os.environ["AZURE_TRANSLATOR_ENDPOINT"],
        credential=AzureKeyCredential(os.environ["AZURE_TRANSLATOR_KEY"]),
        region=os.environ["AZURE_TRANSLATOR_REGION"],
    )
    result = client.translate(content=[text], to=[target_language])
    return result[0].translations[0].text
