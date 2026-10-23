from . import storage_client
from . import storage_models

def get_object_metadata(object_name: str) -> storage_models.ObjectMetadata:
    """Retrieves metadata for a specific object in a GCS bucket."""
    
    gcs_client = storage_client.get_storage_client()
    bucket_name = storage_client.get_default_bucket_name()
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")
    
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.get_blob(object_name)

    if not blob:
        raise FileNotFoundError(f"Object gs://{bucket_name}/{object_name} not found.")

    # The blob object from client.get_blob() contains the metadata
    metadata = storage_models.ObjectMetadata(
        name=blob.name,
        bucket=blob.bucket.name,
        size=blob.size,
        content_type=blob.content_type,
        updated=blob.updated,
        md5_hash=blob.md5_hash,
        crc32c=blob.crc32c,
    )

    return metadata
