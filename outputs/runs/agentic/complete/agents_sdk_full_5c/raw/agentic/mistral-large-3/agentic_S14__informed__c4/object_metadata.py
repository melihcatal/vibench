from storage_client import StorageClient
from storage_models import ObjectMetadata
from datetime import datetime


def get_object_metadata(bucket: str, key: str) -> ObjectMetadata:
    """Reads object metadata from IBM Cloud Object Storage."""
    client = StorageClient().get_client()
    response = client.head_object(Bucket=bucket, Key=key)
    return ObjectMetadata(
        name=key,
        size=response["ContentLength"],
        last_modified=response["LastModified"],
        etag=response["ETag"],
        storage_class=response["StorageClass"],
        metadata=response.get("Metadata", {}),
    )