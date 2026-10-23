from google.cloud import storage

def get_object_metadata(bucket_name, object_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    metadata = blob.metadata
    return metadata