from typing import Optional

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from storage_client import build_blob_service_client, load_storage_config, normalize_container_name


def stored_text_translate(container_name: Optional[str], blob_name: str, target_language: str):
    config = load_storage_config()
    container = normalize_container_name(container_name, config)
    blob = build_blob_service_client(config).get_blob_client(container=container, blob=blob_name)
    text = blob.download_blob().content_as_text()
    client = TextTranslationClient(endpoint=config.account_url, credential=AzureKeyCredential(config.account_key or ""))
    return client.translate(content=[text], to=[target_language])
