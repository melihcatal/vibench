import boto3
import os

def get_aws_translate_client():
    """
    Provides local configuration and client helper utilities for AWS Translate.
    """
    client = boto3.client(
        'translate',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION")
    )
    return client
