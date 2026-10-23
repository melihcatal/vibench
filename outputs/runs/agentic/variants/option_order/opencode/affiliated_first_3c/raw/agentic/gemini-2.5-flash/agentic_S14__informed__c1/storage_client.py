from google.cloud import storage


def get_gcs_client():
    """Returns a Google Cloud Storage client."""
    # Google Cloud Storage client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # environment variable for authentication.
    return storage.Client()
