from google.cloud import storage

def list_prefix(bucket_name, prefix=''):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    for blob in blobs:
        print(blob.name)