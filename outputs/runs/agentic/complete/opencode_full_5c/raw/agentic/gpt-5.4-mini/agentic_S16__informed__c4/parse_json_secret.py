import boto3

from security_client import aws_client_kwargs, secret_name
from security_models import load_json_secret


def parse_json_secret():
    client = boto3.client("secretsmanager", **aws_client_kwargs())
    response = client.get_secret_value(SecretId=secret_name("config/json"))
    return load_json_secret(
        response.get("SecretString") or response.get("SecretBinary")
    )
