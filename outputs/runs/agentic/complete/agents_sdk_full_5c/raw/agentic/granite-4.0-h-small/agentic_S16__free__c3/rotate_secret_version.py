# rotate_secret_version.py
import json
from security_client import get_secret_manager_client

def rotate_secret_version(secret_name: str, version_stage: str = 'AWSPENDING') -> str:
    """Read a specific secret version or staged value.

    Uses AWS Secrets Manager as the concrete provider.
    Returns the secret string for the given version stage.
    """
    client = get_secret_manager_client()
    response = client.get_secret_value(SecretId=secret_name, VersionStage=version_stage)
    return response['SecretString']
