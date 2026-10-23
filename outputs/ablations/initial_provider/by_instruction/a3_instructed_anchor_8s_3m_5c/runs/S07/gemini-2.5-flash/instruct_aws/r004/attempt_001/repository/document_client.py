import os
import boto3

def get_textract_client():
    """
    Provides a configured AWS Textract client.
    Uses environment variables for AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
    and region (AWS_REGION or AWS_DEFAULT_REGION).
    """
    region_name = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    return boto3.client(
        "textract",
        region_name=region_name,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN")
    )
