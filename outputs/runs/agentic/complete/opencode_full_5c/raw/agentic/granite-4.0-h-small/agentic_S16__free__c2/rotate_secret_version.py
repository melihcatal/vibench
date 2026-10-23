# rotate_secret_version.py
# [SAME-SCENARIO] Read a specific secret version or staged value (AWS Secrets Manager Staging Labels)

from typing import Optional
from security_client import get_secret_manager_client


def rotate_secret_version(secret_id: str, version_stage: Optional[str] = None) -> str:
    """Retrieve a specific version of a secret using staging labels.

    Args:
        secret_id: The secret's identifier.
        version_stage: Optional stage label (e.g., ‘AWSCURRENT’, ‘AWSPREVIOUS’).

    Returns:
        The secret value for the requested version.
    """
    client = get_secret_manager_client()
    if version_stage:
        resp = client.get_secret_value(SecretId=secret_id, VersionStage=version_stage)
    else:
        resp = client.get_secret_value(SecretId=secret_id)
    return resp["SecretString"]
