import os

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from storage_client import get_blob_service_client, load_config, normalize_blob_name


def stored_text_translate(blob_name: str, target_language: str, container: str = None) -> str:
    config = load_config(container)
    client = get_blob_service_client(config)
    text = client.get_blob_client(container=config.container, blob=normalize_blob_name(blob_name)).download_blob().content_as_text()
    translation_client = TextTranslationClient(endpoint=os.environ["AZURE_TRANSLATOR_ENDPOINT"], credential=AzureKeyCredential(os.environ["AZURE_TRANSLATOR_KEY"]))
    result = translation_client.translate(content=[text], to=[target_language])
    return result[0].translations[0].text
