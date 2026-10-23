import os
import time
from storage_client import StorageClient
from storage_models import StorageModels

# Use IBM Cloud Object Storage SDK for signed URL generation
s3 = StorageClient().get_service()

def presigned_download(bucket: str, key: str, expires_in_seconds: int = 3600) -> str:
    """Create a time‑limited signed download URL for a stored object (IBM COS)."
    # IBM COS SDK provides a generate_presigned_url method via the underlying botocore client
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expires_in_seconds
    )
    return url

# Example usage (uncomment to test)
# print(presigned_download('my-bucket', 'example.txt'))
