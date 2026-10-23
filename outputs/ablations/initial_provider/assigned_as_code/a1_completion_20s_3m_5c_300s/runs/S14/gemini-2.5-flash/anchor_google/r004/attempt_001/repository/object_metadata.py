from storage_client import get_storage_client
from storage_models import StorageObject

def get_object_metadata(payload: dict) -> StorageObject:
    client = get_storage_client()
    bucket = client.bucket(payload["bucket_name"])
    blob = bucket.get_blob(payload["object_name"])

    if not blob:
        raise ValueError(f"Object {payload['object_name']} not found in bucket {payload['bucket_name']}")

    # Blob.get_blob returns a Blob object which contains metadata.
    # We can convert it to a dictionary for a more generic return type.
    metadata = {
        "name": blob.name,
        "bucket": blob.bucket.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "crc32c": blob.crc32c,
        "md5_hash": blob.md5_hash,
        "generation": blob.generation,
        "metageneration": blob.metageneration,
        "time_created": blob.time_created.isoformat() if blob.time_created else None,
        "updated": blob.updated.isoformat() if blob.updated else None,
        "custom_metadata": blob.metadata, # Custom key-value pairs set by the user
    }
    return metadata
