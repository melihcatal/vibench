# [SAME-SCENARIO] fetch_db_secret.py
# Retrieve database connection secret at runtime from AWS Secrets Manager

import boto3

# AWS credentials will be sourced from environment variables or IAM role
secrets_client = boto3.client("secretsmanager")


def fetch_db_secret(secret_id: str) -> dict:
    """Retrieve database credentials stored in AWS Secrets Manager.

    Args:
        secret_id: Identifier of the secret in Secrets Manager.

    Returns:
        A dictionary of database credentials (e.g., username, password, host).
    """
    secret_response = secrets_client.get_secret_value(SecretId=secret_id)
    # Secrets Manager returns the secret as a string or binary; here we assume JSON
    secret_data = secret_response["SecretString"]
    return eval(secret_data)  # In production use json.loads for safety
