import boto3

def get_object_metadata(bucket_name: str, object_key: str) -> dict:
    """
    Reads object metadata from AWS S3.

    Args:
        bucket_name: The name of the S3 bucket.
        object_key: The key of the object to retrieve metadata for.

    Returns:
        A dictionary containing the object's metadata.
    """
    s3 = boto3.client("s3")
    response = s3.head_object(Bucket=bucket_name, Key=object_key)
    return response
