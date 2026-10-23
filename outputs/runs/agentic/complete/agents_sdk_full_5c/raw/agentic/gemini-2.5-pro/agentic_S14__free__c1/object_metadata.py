from storage_client import get_gcs_client, get_bucket_name
from storage_models import ObjectMetadata

def get_object_metadata(blob_name: str) -> ObjectMetadata:
    """
    Retrieves metadata for a specific object in a GCS bucket.

    Args:
        blob_name (str): The name of the object.

    Returns:
        An ObjectMetadata instance.
    """
    client = get_gcs_client()
    bucket_name = get_bucket_name()
    bucket = client.bucket(bucket_name)
    blob = bucket.get_blob(blob_name)

    if not blob:
        raise FileNotFoundError(f"Object '{blob_name}' not found in bucket '{bucket_name}'.")

    return ObjectMetadata(
        name=blob.name,
        bucket=blob.bucket.name,
        size=blob.size,
        updated=blob.updated,
        content_type=blob.content_type,
        custom_metadata=blob.metadata
    )
