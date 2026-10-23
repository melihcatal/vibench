from google.cloud import storage

def get_object_metadata(bucket_name, object_name):
    """Retrieves metadata for a given object."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    return blob.metadata