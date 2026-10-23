# storage_client.py
import os

# Choose ONE concrete managed object storage provider and import its SDK.
# Here we use Google Cloud Storage as the concrete provider.
try:
    from google.cloud import storage

    SERVICE = "Google Cloud Storage"
except ImportError:
    SERVICE = None
    raise ImportError(
        "Google Cloud Storage SDK not available. Set GOOGLE_APPLICATION_CREDENTIALS env var."
    )


def get_client():
    """Return a configured storage client for the chosen provider."""
    return storage.Client()


def bucket_name():
    """Return the bucket name from environment or default."""
    return os.getenv("OBJECT_STORAGE_BUCKET", "my-test-bucket")


# Helper to normalize object name/path for provider
def normalize_object_name(name):
    return name.strip().replace("\\", "/")
