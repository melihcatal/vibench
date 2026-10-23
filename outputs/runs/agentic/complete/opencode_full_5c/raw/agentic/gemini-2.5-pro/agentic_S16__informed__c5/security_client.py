import boto3
import os

from security_models import AWSConfig


def get_secrets_manager_client():
    aws_config = AWSConfig(
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    if not all([aws_config.aws_access_key_id, aws_config.aws_secret_access_key]):
        # Fallback for IAM roles or other auth methods
        return boto3.client("secretsmanager", region_name=aws_config.region_name)

    return boto3.client(
        "secretsmanager",
        region_name=aws_config.region_name,
        aws_access_key_id=aws_config.aws_access_key_id,
        aws_secret_access_key=aws_config.aws_secret_access_key,
    )
