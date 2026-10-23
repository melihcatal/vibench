import os
import boto3

# AWS Secrets Manager configuration
client = boto3.client(
    "secretsmanager",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


def fetch_db_secret(secret_id: str) -> str:
    """Fetch a database connection secret from AWS Secrets Manager.

    Args:
        secret_id: Identifier of the secret that stores the DB credentials in JSON.

    Returns:
        The secret payload containing username, password, host, port, etc.
    """
    response = client.get_secret_value(SecretId=secret_id)
    # Secret is expected to be a JSON string with keys like username/password/host/port
    return response.get("SecretString")
