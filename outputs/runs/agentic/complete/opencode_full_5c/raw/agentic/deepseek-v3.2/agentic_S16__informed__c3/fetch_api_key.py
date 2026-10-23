import os
import boto3
from botocore.exceptions import ClientError


def fetch_api_key(secret_name: str) -> str:
    """
    Fetch an API key from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret in AWS Secrets Manager

    Returns:
        The API key value as a string
    """
    # AWS provider-specific client
    client = boto3.client(
        "secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            return response["SecretString"]
        else:
            raise ValueError("Secret is not a string")
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise ValueError(f"Secret {secret_name} not found") from e
        elif error_code == "InvalidRequestException":
            raise ValueError(f"Invalid request for secret {secret_name}") from e
        elif error_code == "InvalidParameterException":
            raise ValueError(f"Invalid parameter for secret {secret_name}") from e
        else:
            raise RuntimeError(f"Error retrieving secret {secret_name}: {e}") from e
