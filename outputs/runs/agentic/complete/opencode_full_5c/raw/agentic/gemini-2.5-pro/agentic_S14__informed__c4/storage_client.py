import os
from google.cloud import storage


def get_gcs_client():
    """Initializes and returns a Google Cloud Storage client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    return storage.Client()


def get_storage_bucket(client, bucket_name=None):
    """Gets a bucket from the environment or a provided name."""
    if bucket_name is None:
        bucket_name = os.environ.get("GCS_BUCKET_NAME")
        if not bucket_name:
            raise ValueError(
                "Bucket name must be provided or set in GCS_BUCKET_NAME environment variable."
            )
    return client.get_bucket(bucket_name)
