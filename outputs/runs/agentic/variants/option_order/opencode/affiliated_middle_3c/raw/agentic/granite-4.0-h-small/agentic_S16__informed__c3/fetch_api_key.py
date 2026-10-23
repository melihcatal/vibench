import os
import boto3

# AWS Secrets Manager configuration
client = boto3.client(
    "secretsmanager",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


def fetch_api_key(secret_id: str) -> str:
    """Fetch a plain-text API key from AWS Secrets Manager.

    Args:
        secret_id: Identifier of the secret that stores the API key.

    Returns:
        The API key value.
    """
    response = client.get_secret_value(SecretId=secret_id)
    # secret can be stored as a string or in JSON
    secret_string = response.get("SecretString")
    if secret_string:
        return secret_string
    else:
        # binary data case
        import json

        secret_bytes = response["SecretBinary"]
        secret = json.loads(secret_bytes.decode("utf-8"))
        return secret.get("API_KEY")
