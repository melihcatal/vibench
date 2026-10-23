from storage_client import get_blob_service_client, load_config, normalize_blob_name
from storage_models import MetadataResult


def object_metadata(blob_name: str, container: str = None) -> MetadataResult:
    config = load_config(container)
    client = get_blob_service_client(config)
    blob_client = client.get_blob_client(container=config.container, blob=normalize_blob_name(blob_name))
    props = blob_client.get_blob_properties()
    return MetadataResult(container=config.container, blob=normalize_blob_name(blob_name), size=getattr(props, "size", None), content_type=getattr(props.content_settings, "content_type", None), etag=getattr(props, "etag", None), last_modified=str(getattr(props, "last_modified", None)) if getattr(props, "last_modified", None) else None, metadata=getattr(props, "metadata", None))
