from google.cloud import storage

def get_object_metadata(bucket_name: str, object_name: str):
    """Reads object metadata or head information from Google Cloud Storage.

    Args:
        bucket_name: The name of the GCS bucket.
        object_name: The name of the object within the bucket.

    Returns:
        A dictionary containing the object's metadata.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    blob.reload()  # Fetches the latest metadata

    return blob.metadata
