import boto3


def get_secrets_manager_client():
    """Returns a boto3 Secrets Manager client."""
    return boto3.client("secretsmanager")
