import os
import boto3
from security_client import SecretClient

def fetch_db_secret(secret_id: str) -> dict:
    """Fetches a database connection secret from AWS Secrets Manager.

    The returned dict is expected to contain keys like 'username', 'password', 'host', 'port', 'dbname'.

    Args:
        secret_id: The ARN or friendly name of the secret.

    Returns:
        Parsed secret dictionary.
    """
    client = SecretClient()
    response = client.get_secret_value(SecretId=secret_id)
    # Assume the secret value is a JSON string with DB credentials
    return response['SecretString']
