import os
import json
import base64
import boto3


def fetch_db_secret(secret_id: str | None = None, region_name: str | None = None) -> dict:
    secret_id = secret_id or os.environ.get("AWS_SECRET_NAME") or os.environ.get("DB_SECRET_NAME")
    if not secret_id:
        raise ValueError("Missing secret id; set AWS_SECRET_NAME or DB_SECRET_NAME")
    region = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_id)
    if "SecretString" in response and response["SecretString"]:
        return json.loads(response["SecretString"])
    secret_binary = response.get("SecretBinary")
    if secret_binary is None:
        raise ValueError("Secret value is empty")
    decoded = base64.b64decode(secret_binary)
    return json.loads(decoded.decode("utf-8"))


def get_db_connection_secret() -> dict:
    return fetch_db_secret()
