import os
import json
import boto3


def fetch_db_secret(secret_name: str | None = None, region_name: str | None = None) -> dict:
    secret_name = secret_name or os.environ.get("AWS_SECRET_NAME")
    region_name = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if not secret_name:
        raise ValueError("AWS_SECRET_NAME is required")
    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response.get("SecretString")
    if not secret_string:
        raise ValueError("SecretString is missing")
    return json.loads(secret_string)


def get_database_connection_string(secret_name: str | None = None, region_name: str | None = None) -> str:
    secret = fetch_db_secret(secret_name=secret_name, region_name=region_name)
    if "connection_string" in secret:
        return secret["connection_string"]
    if {"host", "port", "username", "password", "database"}.issubset(secret):
        return f"postgresql://{secret['username']}:{secret['password']}@{secret['host']}:{secret['port']}/{secret['database']}"
    raise KeyError("Secret must include connection_string or host, port, username, password, and database")
