from google.cloud import storage
from storage_client import get_storage_client
from storage_models import StorageObject

def get_object_metadata(obj: StorageObject) -> dict:
    """Reads object metadata or head information from Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(obj.bucket_name)
    blob = bucket.blob(obj.object_name)

    blob.reload()
    metadata = {
        "name": blob.name,
        "bucket": blob.bucket.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "time_created": blob.time_created,
        "updated": blob.updated,
        "etag": blob.etag,
        "crc32c": blob.crc32c,
        "md5_hash": blob.md5_hash,
        "metadata": blob.metadata, # Custom metadata
    }
    print(f"Metadata for {obj.bucket_name}/{obj.object_name}: {metadata}")
    return metadata

if __name__ == '__main__':
    # Example usage (replace with actual values)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up
    # metadata = get_object_metadata(StorageObject(bucket_name="your-bucket-name", object_name="my-test-file.txt"))
    # print(metadata)
    pass
