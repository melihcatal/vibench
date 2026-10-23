import os

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def stored_text_translate(text: str, target_language: str):
    client = TextTranslationClient(endpoint=os.environ["AZURE_TRANSLATOR_ENDPOINT"], credential=AzureKeyCredential(os.environ["AZURE_TRANSLATOR_KEY"]))
    return client.translate(content=[text], to=[target_language], from_parameter=None)
