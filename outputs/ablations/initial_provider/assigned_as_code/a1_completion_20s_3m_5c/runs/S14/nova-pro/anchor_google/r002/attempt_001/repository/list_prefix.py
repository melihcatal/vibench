from google.cloud import storage

def list_objects(bucket_name, prefix=''):
    """Lists objects in a bucket with a given prefix."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    return [blob.name for blob in blobs]