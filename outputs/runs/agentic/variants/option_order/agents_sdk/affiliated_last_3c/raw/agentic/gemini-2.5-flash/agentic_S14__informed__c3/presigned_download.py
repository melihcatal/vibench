from storage_client import get_s3_client

def create_presigned_download_url(bucket_name: str, object_key: str, expiration_seconds: int = 3600) -> str:
    """
    Creates a time-limited signed download URL for an object in Amazon S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The key (path) of the object in the bucket.
        expiration_seconds (int): The number of seconds the URL is valid for.

    Returns:
        str: The pre-signed URL.
    """
    s3_client = get_s3_client()
    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_key
        },
        ExpiresIn=expiration_seconds
    )
    return url
