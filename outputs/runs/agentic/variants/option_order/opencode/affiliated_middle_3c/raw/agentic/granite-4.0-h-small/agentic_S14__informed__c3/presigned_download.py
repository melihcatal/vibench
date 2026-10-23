import boto3
from botocore.client import Config


def create_presigned_download_url(bucket_name, object_key, expiration_seconds=3600):
    """Generate a presigned URL for downloading an object from Amazon S3.

    The AWS provider is identified by the boto3 import and AWS_* environment
    variables. The URL expires after ``expiration_seconds`` (default 1 hour).
    """
    s3 = boto3.client("s3", config=Config(signature_version="s3v4"))
    try:
        response = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration_seconds,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to create presigned URL: {e}")
    return response

    print(
        f"Presigned download URL for {object_key} expires in {expiration_seconds} seconds"
    )
