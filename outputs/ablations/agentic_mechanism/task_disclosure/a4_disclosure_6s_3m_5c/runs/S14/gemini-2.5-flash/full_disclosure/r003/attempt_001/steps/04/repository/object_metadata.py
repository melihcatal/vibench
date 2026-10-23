import boto3
import os

def get_object_metadata(bucket_name: str, object_key: str) -> dict:
    """
    Reads object metadata or head information from Amazon S3.

    Args:
        bucket_name: The name of the S3 bucket.
        object_key: The key of the object in the S3 bucket.

    Returns:
        A dictionary containing the object's metadata.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.environ.get('AWS_SESSION_TOKEN')
    )
    response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
    return response.get('Metadata', {})

