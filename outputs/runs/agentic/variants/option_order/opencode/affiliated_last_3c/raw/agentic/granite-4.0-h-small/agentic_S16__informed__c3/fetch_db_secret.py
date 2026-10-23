import os
import boto3

# AWS Secrets Manager


def fetch_db_secret(secret_id: str) -> dict:
    """Fetch a database connection secret from AWS Secrets Manager.

    Returns a dictionary containing the secret fields (e.g. username, password, host).
    """
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_id)
    secret = response["SecretString"]
    return json.loads(secret)
