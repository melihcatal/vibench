from typing import Optional

from storage_client import build_blob_service_client, normalize_container_name
from storage_models import StorageObjectMetadata


def object_metadata(container_name: Optional[str], blob_name: str) -> StorageObjectMetadata:
    client = build_blob_service_client()
    container = normalize_container_name(container_name)
    props = client.get_blob_client(container=container, blob=blob_name).get_blob_properties()
    return StorageObjectMetadata(
        container_name=container,
        blob_name=blob_name,
        etag=str(props.etag) if props.etag else None,
        last_modified=props.last_modified.isoformat() if props.last_modified else None,
        content_length=props.size,
        content_type=getattr(props.content_settings, "content_type", None),
        metadata=dict(props.metadata or {}),
    )
