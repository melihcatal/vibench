import boto3
import os

def get_s3_client():
    """
    Initializes and returns a boto3 S3 client.
    AWS credentials and region are typically configured via environment variables
    (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION) or AWS config files.
    """
    try:
        s3_client = boto3.client('s3')
        return s3_client
    except Exception as e:
        print(f"Error initializing S3 client: {e}")
        return None

