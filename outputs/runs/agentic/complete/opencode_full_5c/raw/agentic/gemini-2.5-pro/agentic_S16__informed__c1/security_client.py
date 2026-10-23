import boto3
import os


def get_secrets_manager_client():
    """
    Initializes and returns a Boto3 Secrets Manager client.

    Expects AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) and
    AWS_REGION to be configured in the environment.
    """
    return boto3.client(
        "secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
