import boto3


def get_secrets_client():
    return boto3.client("secretsmanager")


def get_secret(secret_name):
    client = get_secrets_client()
    response = client.get_secret_value(SecretId=secret_name)
    return response["SecretString"]
