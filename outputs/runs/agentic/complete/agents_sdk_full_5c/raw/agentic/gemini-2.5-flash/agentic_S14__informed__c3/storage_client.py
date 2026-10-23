import boto3
import os

def get_s3_client():
    """
    Returns a configured boto3 S3 client.
    Assumes AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION
    are set as environment variables.
    """
    # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are implicitly picked up by boto3
    # AWS_REGION is also implicitly picked up or can be passed
    return boto3.client(
        's3',
        region_name=os.getenv('AWS_REGION', 'us-east-1') # Default region
    )
