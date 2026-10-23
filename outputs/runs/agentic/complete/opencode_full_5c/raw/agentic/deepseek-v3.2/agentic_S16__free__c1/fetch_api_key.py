import os
import boto3
from botocore.exceptions import ClientError


def fetch_api_key(secret_name: str) -> str:
    """
    Fetch an API key from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret in AWS Secrets Manager

    Returns:
        The API key as a string
    """
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            return response["SecretString"]
        else:
            raise ValueError("Secret is not in string format")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise ValueError(f"Secret {secret_name} not found") from e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise ValueError(f"Invalid request for secret {secret_name}") from e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise ValueError(f"Invalid parameter for secret {secret_name}") from e
        else:
            raise RuntimeError(f"Error retrieving secret {secret_name}: {e}") from e
