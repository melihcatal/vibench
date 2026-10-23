import boto3

def get_s3_client(region_name: str):
    """
    Provides a configured boto3 S3 client.

    Args:
        region_name (str): The AWS region to connect to (e.g., 'us-east-1').

    Returns:
        boto3.client: An initialized S3 client.
    """
    s3_client = boto3.client('s3', region_name=region_name)
    return s3_client
