from google.cloud import storage
from google.api_core.exceptions import NotFound


def object_metadata(bucket_name: str, object_name: str) -> dict:
    """
    Reads object metadata or head information from Google Cloud Storage.

    Args:
        bucket_name: Name of the GCS bucket.
        object_name: Name of the object to fetch metadata for.

    Returns:
        A dictionary containing the object's metadata.

    Raises:
        NotFound: If the object does not exist.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    if not blob.exists():
        raise NotFound(f"Object {object_name} not found in bucket {bucket_name}.")

    blob.reload()  # Ensure metadata is fresh
    return {
        "name": blob.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "time_created": blob.time_created,
        "updated": blob.updated,
        "metadata": blob.metadata or {},
        "etag": blob.etag,
        "generation": blob.generation,
    }
