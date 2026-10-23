import boto3

def get_s3_client():
    """Returns a boto3 S3 client."""
    return boto3.client('s3')