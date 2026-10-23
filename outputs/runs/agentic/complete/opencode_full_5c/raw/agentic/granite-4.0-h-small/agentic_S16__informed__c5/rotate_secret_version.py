import os
from ibm_watsonx_ai import SecretManagerClient
from ibm_watsonx_ai.auth import get_auth_header_from_env


def fetch_secret_version(secret_id: str = "deploy-key", version: int = 1):
    """Read a specific version (or staged) value of a secret from IBM Cloud Secrets Manager.

    Args:
        secret_id: Identifier of the secret.
        version: Version number (or 'staged') to retrieve.

    Returns:
        The secret payload as a dict.
    """
    auth_header = get_auth_header_from_env()
    client = SecretManagerClient(auth_header=auth_header)
    response = client.get_secret(secret_id=secret_id, version=version)
    return response.get_secret()
