from typing import Optional

from openai import OpenAI

from storage_client import build_blob_service_client, normalize_container_name


def stored_asset_summary(container_name: Optional[str], blob_name: str):
    container = normalize_container_name(container_name)
    blob = build_blob_service_client().get_blob_client(container=container, blob=blob_name)
    text = blob.download_blob().content_as_text()
    client = OpenAI()
    return client.responses.create(model="gpt-5.4-mini", input=text)
