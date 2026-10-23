import os
from google.cloud import storage

def get_gcs_client():
    """
    Initializes and returns a Google Cloud Storage client.
    
    Relies on Google Cloud SDK default credential discovery.
    Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    try:
        client = storage.Client()
        return client
    except Exception as e:
        print(f"Failed to create GCS client: {e}")
        raise

def get_bucket_name():
    """
    Retrieves the GCS bucket name from an environment variable.
    """
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")
    return bucket_name
