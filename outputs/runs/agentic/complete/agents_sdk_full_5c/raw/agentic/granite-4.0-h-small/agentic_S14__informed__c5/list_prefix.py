import os
from google.cloud import storage

def list_objects_with_prefix(bucket_name, prefix, delimiter=None):
    """List objects in a GCS bucket under a given prefix (optional delimiter for folder-like listing)."
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
    return [blob.name for blob in blobs]
