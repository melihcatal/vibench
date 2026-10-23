from google.cloud import storage

def object_metadata(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    metadata = blob.metadata
    print(f"Metadata for {blob_name}: {metadata}")
    return metadata
