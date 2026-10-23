from azure.storage.blob import BlobClient

from storage_client import load_storage_config, resolve_container_path
from storage_models import MetadataResult, normalize_metadata


def object_metadata(object_name):
    config = load_storage_config()
    blob = BlobClient.from_blob_url(resolve_container_path(object_name, config), credential=None)
    props = blob.get_blob_properties()
    return MetadataResult(
        object_name=object_name,
        metadata=normalize_metadata(getattr(props, "metadata", None)),
        content_type=getattr(props.content_settings, "content_type", None),
        content_length=getattr(props, "size", None),
    )
