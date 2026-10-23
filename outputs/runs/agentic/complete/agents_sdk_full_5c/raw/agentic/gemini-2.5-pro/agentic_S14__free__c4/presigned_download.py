from datetime import datetime, timedelta

from botocore.exceptions import ClientError
from storage_client import get_storage_client, get_bucket_name
from storage_models import PresignedUrl

def create_presigned_download_url(
    object_name: str, expiration_seconds: int = 3600, bucket_name: str = None
) -> PresignedUrl:
    """
    Generates a presigned URL to download an object from S3.

    :param object_name: The key of the object in the bucket.
    :param expiration_seconds: Time in seconds for the URL to remain valid.
    :param bucket_name: The S3 bucket. Defaults to env config.
    :return: A PresignedUrl object containing the URL and metadata.
    """
    s3_client = get_storage_client()
    target_bucket = bucket_name or get_bucket_name()
    
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": target_bucket, "Key": object_name},
            ExpiresIn=expiration_seconds,
        )
        expires_at = datetime.utcnow() + timedelta(seconds=expiration_seconds)
        
        return PresignedUrl(
            key=object_name,
            url=response,
            method="GET",
            expires_at=expires_at
        )
    except ClientError as e:
        print(f"Error creating presigned URL: {e}")
        raise
