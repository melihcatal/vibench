from google.cloud import storage
from storage_client import get_storage_client
from storage_models import StorageObject

def create_presigned_download_url(obj: StorageObject, expiration_seconds: int = 3600) -> str:
    """Creates a time-limited signed download URL for a stored object in Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(obj.bucket_name)
    blob = bucket.blob(obj.object_name)

    url = blob.generate_signed_url(expiration=expiration_seconds, method='GET')
    print(f"Generated signed URL for {obj.bucket_name}/{obj.object_name}: {url}")
    return url

if __name__ == '__main__':
    # Example usage (replace with actual values)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up
    # url = create_presigned_download_url(StorageObject(bucket_name="your-bucket-name", object_name="my-test-file.txt"))
    # print(f"Presigned URL: {url}")
    pass
