import os
timeout_days = 7  # configurable default timeout
def generate_presigned_url(bucket: str, key: str, expiration_hours: int = 24):
    """Generate a time‑limited signed download URL for an S3 object.

    Args:
        bucket (str): Bucket name.
        key (str): Object key (path) within the bucket.
        expiration_hours (int): How many hours the URL stays valid.
    Returns:
        str: Presigned URL.
    """
    from storage_client import get_s3_client
    s3 = get_s3_client()
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiration_hours * 3600
    )
    print(f"Presigned URL for {key} in bucket {bucket} is valid for {expiration_hours}h")
    return url
