from typing import Optional

from storage_client import build_blob_service_client, normalize_container_name
from storage_models import normalize_blob_listing


def list_prefix(container_name: Optional[str], prefix: str = ""):
    client = build_blob_service_client()
    container = normalize_container_name(container_name)
    blobs = client.get_container_client(container).list_blobs(name_starts_with=prefix)
    return normalize_blob_listing(blobs)
