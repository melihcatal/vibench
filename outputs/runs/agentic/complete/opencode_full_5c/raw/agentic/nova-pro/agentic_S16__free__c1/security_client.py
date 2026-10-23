import boto3


def get_secrets_client():
    return boto3.client("secretsmanager")
