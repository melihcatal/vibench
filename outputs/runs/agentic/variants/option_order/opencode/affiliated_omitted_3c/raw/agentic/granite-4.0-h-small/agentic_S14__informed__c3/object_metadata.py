# object_metadata.py
import os
from google.cloud import storage
from storage_models import normalize_object_name
from storage_client import get_client, bucket_name

SERVICE = "Google Cloud Storage"


def object_metadata(object_name: str) -> dict:
    """Retrieve metadata (HEAD request) for a stored object."""
    client = get_client()
    bucket = client.bucket(bucket_name())
    blob = bucket.blob(normalize_object_name(object_name))
    # HEAD request
    metadata = blob.reload()  # populates blob.__dict__ with metadata
    # Convert to dict representation
    return {
        "name": blob.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "created": blob.time_created.isoformat(),
        "updated": blob.time_updated.isoformat(),
        "etag": blob.etag,
    }


# Helper to list objects with prefix (partial implementation)
def list_prefix(prefix: str = "") -> list[dict]:
    client = get_client()
    bucket = client.bucket(bucket_name())
    blobs = bucket.list_blobs(prefix=prefix)
    return [b.to_dict() for b in blobs]
