from datetime import timedelta

from storage_client import get_storage_client, get_bucket_name
from storage_models import PresignedDownloadPayload, StorageConfig

def presigned_download(payload: PresignedDownloadPayload, config: Optional[StorageConfig] = None) -> dict:
    client = get_storage_client(config)
    bucket_name = get_bucket_name(config)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(payload.object_name)
    
    # Generate the signed URL
    # The URL is valid for the specified number of seconds
    signed_url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(seconds=payload.expiration_seconds),
        method="GET",
    )
    
    return {"presigned_url": signed_url}
