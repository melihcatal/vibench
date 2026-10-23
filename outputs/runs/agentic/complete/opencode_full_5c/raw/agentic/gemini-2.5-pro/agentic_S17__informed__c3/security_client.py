import os
import boto3


def get_kms_client():
    """
    Initializes and returns a boto3 client for AWS Key Management Service (KMS).

    Reads AWS credentials and region from environment variables.
    Make sure to set:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not all([aws_access_key_id, aws_secret_access_key]):
        raise ValueError(
            "AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) were not found in environment variables."
        )

    return boto3.client(
        "kms",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
