import os

from google.cloud import storage

def get_storage_client():
    """Returns a storage client configured with the project ID."""
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    return storage.Client(project=project_id)

def get_bucket(client, bucket_name):
    """Returns a bucket object for the given bucket name."""
    return client.bucket(bucket_name)

def get_blob(bucket, object_name):
    """Returns a blob object for the given object name."""
    return bucket.blob(object_name)