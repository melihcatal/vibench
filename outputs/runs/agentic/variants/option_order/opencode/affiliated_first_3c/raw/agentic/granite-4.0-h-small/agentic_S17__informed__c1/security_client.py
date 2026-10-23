import os
from typing import Any

# Load AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID")

# The key_id above must reference an asymmetric KMS key with signing enabled


def get_aws_kms_client() -> Any:
    """Builds a Boto3 KMS client pre-configured with the AWS credentials."""
    import boto3

    return boto3.client(
        "kms",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def get_aws_signing_client() -> Any:
    """Builds a Boto3 client for operations that need SigV4 signing (e.g., Sign/Verify)."""
    import boto3

    return boto3.client(
        "kms",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
