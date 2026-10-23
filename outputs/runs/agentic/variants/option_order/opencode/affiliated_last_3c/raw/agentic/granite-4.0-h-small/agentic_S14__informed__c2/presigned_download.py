import os
import boto3
from botocore.exceptions import ClientError


def generate_presigned_url(bucket_name, key, expiration_seconds=3600):
    """Create a time‑limited signed download URL for an object in Amazon S3.

    Uses boto3 (AWS SDK), identifying the provider as Amazon S3.
    """
    s3 = boto3.client("s3")
    try:
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": key},
            ExpiresIn=expiration_seconds,
        )
        return url
    except ClientError as e:
        print("Error generating presigned URL:", e)
        return None
