import os
import boto3


def get_storage_client():
    """
    Provides a boto3 S3 client configured from environment variables.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not all([aws_access_key_id, aws_secret_access_key]):
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set")

    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )


def get_textract_client():
    """
    Provides a boto3 Textract client configured from environment variables.
    """
    return boto3.client(
        "textract", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )


def get_translate_client():
    """
    Provides a boto3 Translate client configured from environment variables.
    """
    return boto3.client(
        "translate", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )


def get_bedrock_runtime_client():
    """
    Provides a boto3 Bedrock Runtime client configured from environment variables.
    """
    return boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
