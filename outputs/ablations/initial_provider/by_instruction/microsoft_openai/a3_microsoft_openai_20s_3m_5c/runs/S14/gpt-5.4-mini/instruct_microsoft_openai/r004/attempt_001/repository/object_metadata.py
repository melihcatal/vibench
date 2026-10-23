from storage_client import get_blob_client
from storage_models import StorageMetadataResponse, StorageObjectRef


def object_metadata(bucket: str, object_name: str) -> StorageMetadataResponse:
    ref = StorageObjectRef(bucket=bucket, object_name=object_name)
    props = get_blob_client(ref.bucket, ref.object_name).get_blob_properties()
    return StorageMetadataResponse(bucket=ref.bucket, object_name=ref.object_name, metadata={"size": props.size, "content_type": props.content_settings.content_type, "etag": props.etag, "last_modified": props.last_modified})
