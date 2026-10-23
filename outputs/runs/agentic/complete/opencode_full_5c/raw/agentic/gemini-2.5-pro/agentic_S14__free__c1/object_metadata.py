from storage_client import get_storage_client
from storage_models import ObjectMetadata


def get_object_metadata(bucket_name: str, blob_name: str) -> ObjectMetadata:
    """Gets blob metadata."""
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(blob_name)

    if not blob:
        raise ValueError(f"Blob {blob_name} not found in bucket {bucket_name}")

    metadata = ObjectMetadata(
        name=blob.name,
        bucket=blob.bucket.name,
        size=blob.size,
        content_type=blob.content_type,
        time_created=blob.time_created,
        custom_metadata=blob.metadata,
    )

    print(f"Metadata for {blob_name}:")
    print(metadata.model_dump_json(indent=2))

    return metadata
