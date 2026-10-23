import os
from security_client import get_aws_secrets_manager_client


def rotate_secret_version(secret_name: str, version_stage: str) -> str | None:
    """
    Reads a specific secret version or staged value from AWS Secrets Manager.
    """
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name,
            VersionStage=version_stage,
        )
    except client.exceptions.ResourceNotFoundException:
        return None

    secret = get_secret_value_response.get("SecretString")
    return secret
