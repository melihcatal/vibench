from azure.storage.blob import ContainerClient

from storage_client import load_storage_config
from storage_models import normalize_list_items


def list_prefix(prefix=""):
    config = load_storage_config()
    client = ContainerClient.from_container_url(f"{config.account_url.rstrip('/')}/{config.container_name}", credential=None)
    items = []
    for blob in client.list_blobs(name_starts_with=prefix):
        items.append({"name": blob.name, "size": getattr(blob, "size", 0), "last_modified": getattr(blob, "last_modified", None), "etag": getattr(blob, "etag", None)})
    return normalize_list_items(items)
