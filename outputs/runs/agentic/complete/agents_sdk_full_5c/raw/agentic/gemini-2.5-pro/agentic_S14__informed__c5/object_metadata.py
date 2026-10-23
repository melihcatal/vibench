from google.cloud import storage
from storage_client import get_storage_client, get_bucket_name
from storage_models import ObjectMetadata

def get_object_metadata(object_name: str) -> ObjectMetadata:
    """Gets the metadata for an object in Google Cloud Storage."""
    storage_client = get_storage_client()
    bucket_name = get_bucket_name()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(object_name)

    if not blob:
        raise ValueError(f"Object {object_name} not found in bucket {bucket_name}")

    metadata = ObjectMetadata(
        name=blob.name,
        bucket=blob.bucket.name,
        size=blob.size,
        content_type=blob.content_type,
        updated=blob.updated,
        md5_hash=blob.md5_hash,
        crc32c=blob.crc32c
    )
    print(f"Metadata for {object_name}: {metadata}")
    return metadata
