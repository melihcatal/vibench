from typing import Optional

from openai import OpenAI

from storage_client import build_blob_service_client, normalize_container_name


def asset_metadata_embedding(container_name: Optional[str], blob_name: str):
    container = normalize_container_name(container_name)
    blob_client = build_blob_service_client().get_blob_client(container=container, blob=blob_name)
    props = blob_client.get_blob_properties()
    text = blob_client.download_blob().content_as_text()
    payload = f"{blob_name}\n{props.metadata or {}}\n{text}"
    client = OpenAI()
    return client.embeddings.create(model="text-embedding-3-large", input=payload)
