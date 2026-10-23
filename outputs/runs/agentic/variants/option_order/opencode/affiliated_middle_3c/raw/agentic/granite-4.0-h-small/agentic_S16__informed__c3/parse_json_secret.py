import json
import os
import boto3

# AWS Secrets Manager configuration
client = boto3.client(
    "secretsmanager",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


def parse_json_secret(secret_id: str, field: str = "value") -> str:
    """Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.

    Args:
        secret_id: The ARN or name of the secret.
        field: The key within the JSON payload to extract.

    Returns:
        The value of the specified field.
    """
    response = client.get_secret_value(SecretId=secret_id)
    secret_str = response.get("SecretString")
    if not secret_str:
        raise ValueError("Secret does not contain SecretString")
    secret = json.loads(secret_str)
    return secret.get(field)
