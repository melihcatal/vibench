from google.cloud import storage

def list_objects_with_prefix(bucket_name, prefix):
    """Lists all the objects in the given bucket with the given prefix."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix)

    print(f"Objects in bucket {bucket_name} with prefix {prefix}:")
    for blob in blobs:
        print(blob.name)

if __name__ == "__main__":
    # Replace with your bucket name and prefix
    YOUR_BUCKET_NAME = "your-gcs-bucket-name"  
    YOUR_PREFIX = "your/prefix/"  

    list_objects_with_prefix(YOUR_BUCKET_NAME, YOUR_PREFIX)