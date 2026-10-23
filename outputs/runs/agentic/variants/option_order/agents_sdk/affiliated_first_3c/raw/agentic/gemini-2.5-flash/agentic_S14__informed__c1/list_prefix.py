from google.cloud import storage
from storage_client import get_storage_client

def list_objects_with_prefix(bucket_name: str, prefix: str = "") -> list[str]:
    """Lists stored objects under a Google Cloud Storage bucket with an optional prefix."""
    client = get_storage_client()
    bucket = client.bucket(bucket_name)

    blobs = client.list_blobs(bucket, prefix=prefix)
    object_names = [blob.name for blob in blobs]

    print(f"Objects in {bucket_name} with prefix '{prefix}': {object_names}")
    return object_names

if __name__ == '__main__':
    # Example usage (replace with actual values)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up
    # objects = list_objects_with_prefix(bucket_name="your-bucket-name", prefix="my-folder/")
    # print(objects)
    pass
