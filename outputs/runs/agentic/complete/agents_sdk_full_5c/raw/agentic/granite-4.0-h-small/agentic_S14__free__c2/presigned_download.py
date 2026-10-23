import os
import boto3
from presign_url_expiry import get_presigned_url_expiry
from storage_client import get_s3_client
from storage_models import StoragePresignResponse, StorageUploadResponse

def presigned_download(bucket_name, object_key, expires_in=3600):
    """Create a time-limited signed URL for downloading an object from S3."""
    s3 = get_s3_client()
    response: StoragePresignResponse = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=expires_in,
        HttpMethod='GET'
    )
    # Normalized wrapper
    return StoragePresignResponse({'url': response, 'expires_in': expires_in})
