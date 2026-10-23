import os
import json
import boto3


def fetch_db_secret(secret_name: str = "db-credentials") -> dict:
    """Fetch a database secret from AWS Secrets Manager.

    Returns a dict with keys: username, password, host, dbname, port.
    """
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response["SecretString"])
    return secret
