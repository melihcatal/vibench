from azure.storage.blob import BlobClient

from storage_client import coerce_bytes, load_storage_config, resolve_container_path
from storage_models import UploadResult


def upload_object(object_name, data, content_type=None, metadata=None):
    config = load_storage_config()
    blob = BlobClient.from_blob_url(resolve_container_path(object_name, config), credential=None)
    payload = coerce_bytes(data)
    blob.upload_blob(payload, overwrite=True, content_type=content_type, metadata=metadata)
    props = blob.get_blob_properties()
    return UploadResult(object_name=object_name, etag=getattr(props, "etag", None), url=blob.url)
