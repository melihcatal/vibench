from storage_client import StorageClient


def get_object_metadata(bucket_name: str, blob_name: str) -> dict:
    """Retrieves the metadata for a blob from Google Cloud Storage."""
    storage_client = StorageClient.get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.reload()

    metadata = {
        "name": blob.name,
        "bucket": blob.bucket.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "time_created": blob.time_created.isoformat() if blob.time_created else None,
        "updated": blob.updated.isoformat() if blob.updated else None,
        "md5_hash": blob.md5_hash,
        "crc32c": blob.crc32c,
        "etag": blob.etag,
        "custom_metadata": blob.metadata,  # Custom metadata set by user
    }

    print(f"Metadata for {blob_name} in bucket {bucket_name}: {metadata}")
    return metadata
