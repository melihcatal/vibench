import os
from google.cloud import storage

def get_object_metadata(bucket_name, blob_name):
    """Retrieve metadata/HEAD information for a GCS object.

    bucket_name: str - GCS bucket name
    blob_name: str - object name
    Returns:
        dict - metadata returned by GCS API
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    metadata = blob.reload()  # triggers HEAD request
    # Return a simplified dict representation
    return {
        "name": blob.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "updated": blob.updated,
        "metadata": blob.metadata or {}
    }
