from storage_client import get_s3_client

def create_presigned_download_url(bucket: str, key: str, expiration: int = 3600) -> str:
    """
    Creates a presigned URL for downloading an object from S3.
    
    Args:
        bucket: S3 bucket name
        key: Object key
        expiration: URL validity in seconds
    """
    s3 = get_s3_client()
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiration
    )
    return url