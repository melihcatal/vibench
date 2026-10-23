from google.cloud import storage

def get_storage_client():
    from google.auth import default
    credentials, project = default()
    return storage.Client(credentials=credentials)

def get_bucket(client, bucket_name):
    return client.bucket(bucket_name)

def get_blob(bucket, blob_name):
    return bucket.blob(blob_name)
