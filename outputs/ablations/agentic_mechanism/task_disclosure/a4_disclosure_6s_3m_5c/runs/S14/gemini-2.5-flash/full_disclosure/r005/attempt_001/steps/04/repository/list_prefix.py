from google.cloud import storage

def list_objects_with_prefix(bucket_name: str, prefix: str):
    """Lists all objects in a bucket with a given prefix.

    Args:
        bucket_name: The name of your Cloud Storage bucket.
        prefix: The prefix of the objects to list.
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix)
    
    # You can process the blobs here, for example, print their names
    # for blob in blobs:
    #     print(blob.name)

    return blobs
