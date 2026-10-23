from storage_client import get_s3_client

def get_object_head(bucket: str, key: str):
    """Retrieve HEAD metadata for an S3 object.
    Args:
        bucket (str): Bucket name.
        key (str): Object key.
    Returns:
        dict: Response metadata.
    """
    s3 = get_s3_client()
    response = s3.head_object(Bucket=bucket, Key=key)
    return response
