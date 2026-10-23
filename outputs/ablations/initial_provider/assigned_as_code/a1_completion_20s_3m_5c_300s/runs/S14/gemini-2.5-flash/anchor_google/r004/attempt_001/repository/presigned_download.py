from datetime import timedelta
from storage_client import get_storage_client
from storage_models import StoragePresignedUrl

def presigned_download(payload: dict) -> StoragePresignedUrl:
    client = get_storage_client()
    bucket = client.bucket(payload["bucket_name"])
    blob = bucket.blob(payload["object_name"])

    # Generate a V4 presigned URL for downloading a blob.
    # The URL is valid for 7 days.
    expiration = timedelta(days=7)
    download_url = blob.generate_signed_url(version="v4", expiration=expiration)
    
    return {"download_url": download_url}
