import os

def get_storage_client():
    return storage.Client(project=os.getenv('GOOGLE_CLOUD_PROJECT'))

def get_bucket(client, bucket_name):
    return client.bucket(bucket_name)

def get_blob(bucket, object_name):
    return bucket.blob(object_name)