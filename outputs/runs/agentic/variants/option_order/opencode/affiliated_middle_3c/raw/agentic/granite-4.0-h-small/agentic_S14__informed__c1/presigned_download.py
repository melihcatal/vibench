import boto3
from storage_client import get_s3_client


def create_presigned_download_url(bucket_name, object_key, expiration_seconds=3600):
    """Generate a time-limited signed URL for downloading an S3 object.

    Uses boto3 client from storage_client.get_s3_client(), relying on
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env vars.
    """
    s3 = get_s3_client()
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=expiration_seconds,
    )
