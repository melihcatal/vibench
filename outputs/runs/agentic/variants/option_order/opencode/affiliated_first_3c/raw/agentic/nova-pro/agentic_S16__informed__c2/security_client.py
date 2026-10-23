import boto3


def create_security_client():
    return boto3.client("secretsmanager")
