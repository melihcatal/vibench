import boto3

def get_storage_client():
    """
    Returns a configured boto3 S3 client for Amazon S3.
    Assumes AWS credentials are set via environment variables or AWS config.
    """
    return boto3.client('s3')