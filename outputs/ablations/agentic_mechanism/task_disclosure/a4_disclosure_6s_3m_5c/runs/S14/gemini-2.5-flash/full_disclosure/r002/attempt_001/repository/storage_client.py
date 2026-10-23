from google.cloud import storage

def get_gcs_client():
    """Provides a Google Cloud Storage client."""
    return storage.Client()

def get_gcs_bucket(bucket_name: str):
    """Provides a Google Cloud Storage bucket object."""
    client = get_gcs_client()
    return client.get_bucket(bucket_name)
