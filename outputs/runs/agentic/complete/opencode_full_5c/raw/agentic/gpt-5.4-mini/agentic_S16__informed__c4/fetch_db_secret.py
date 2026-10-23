import boto3

from security_client import aws_client_kwargs, secret_name
from security_models import connection_string_from_secret, load_json_secret


def fetch_db_secret():
    client = boto3.client("secretsmanager", **aws_client_kwargs())
    response = client.get_secret_value(SecretId=secret_name("database/connection"))
    secret_text = response.get("SecretString") or response.get("SecretBinary")
    return connection_string_from_secret(
        load_json_secret(secret_text) if isinstance(secret_text, str) else secret_text
    )
