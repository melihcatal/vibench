import boto3

from security_client import aws_client_kwargs, secret_name


def fetch_api_key():
    client = boto3.client("secretsmanager", **aws_client_kwargs())
    response = client.get_secret_value(SecretId=secret_name("api/key"))
    return response.get("SecretString") or response.get("SecretBinary")
