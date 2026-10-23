from google.cloud import storage

def list_prefix(bucket_name, prefix):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
    for blob in blobs:
        print(blob.name)
