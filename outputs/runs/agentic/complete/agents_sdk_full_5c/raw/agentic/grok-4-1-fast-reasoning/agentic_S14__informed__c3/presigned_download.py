from storage_client import get_storage_client

def presigned_download_url(bucket: str, key: str, expiration: int = 3600) -> str:
    """
    Creates a presigned URL for downloading an object from Amazon S3.
    """
    client = get_storage_client()
    url = client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiration
    )
    return url