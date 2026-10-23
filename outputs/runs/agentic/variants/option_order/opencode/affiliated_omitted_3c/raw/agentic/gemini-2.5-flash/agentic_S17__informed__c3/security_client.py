import os
import boto3


def get_kms_client():
    """Initializes and returns an AWS KMS client."""
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION are expected to be set as environment variables
    kms_client = boto3.client(
        "kms",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    return kms_client
