"""Fetch an API key from AWS Secrets Manager."""

import os
import boto3
from botocore.exceptions import ClientError


def fetch_api_key(secret_name: str, region: str = "us-east-1") -> str:
    """Fetch an API key stored in AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret.
        region: AWS region for Secrets Manager.

    Returns:
        The secret string value (the API key).

    Raises:
        ValueError: If required AWS credentials are not configured.
        ClientError: If the secret cannot be retrieved.
    """
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set"
        )

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as exc:
        raise ClientError(
            exc.response.get("Error", {}),
            f"Failed to fetch secret '{secret_name}' from AWS Secrets Manager",
        ) from exc

    return response["SecretString"]


if __name__ == "__main__":
    name = os.environ.get("SECRET_NAME", "prod/api-key")
    print(fetch_api_key(name))
