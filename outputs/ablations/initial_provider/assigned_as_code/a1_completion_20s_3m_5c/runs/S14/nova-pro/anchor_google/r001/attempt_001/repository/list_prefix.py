from google.cloud import storage

def list_objects(bucket_name, prefix=''):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = storage_client.list_blobs(bucket, prefix=prefix)
    return [blob.name for blob in blobs]