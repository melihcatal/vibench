from google.cloud import storage

def get_storage_client():
    """Initializes and returns a Google Cloud Storage client."""
    return storage.Client()
