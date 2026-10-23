import os
from storage_client import get_s3_client

def create_presigned_download_url(
    bucket_name: str,
    object_key: str,
    expiration_seconds: int = 3600
) -> str:
    """
    Generates a presigned URL for downloading an S3 object.

    Args:
        bucket_name: The name of the S3 bucket.
        object_key: The key (path) of the object.
        expiration_seconds: The number of seconds the URL is valid for (default is 1 hour).

    Returns:
        A string containing the presigned URL.
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration_seconds
        )
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        raise
    return response
