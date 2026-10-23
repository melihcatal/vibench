import boto3
from security_client import SecretClient

def rotate_secret_version(secret_id: str, version_id: str) -> dict:
    """Reads a specific version (or staged value) of a secret from AWS Secrets Manager.

    Args:
        secret_id: ARN or friendly name of the secret.
        version_id: Version ID or 'AWSCURRENT' for the live version.

    Returns:
        The secret version data as returned by Secrets Manager.
    """
    client = SecretClient()
    # The GetSecretValue API can fetch a specific version via VersionStage
    response = client.get_secret_value(SecretId=secret_id, VersionStage=version_id)
    return response['SecretString']
