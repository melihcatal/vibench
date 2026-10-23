from security_client import SecretManagerClient


def rotate_secret_version(secret_id: str, version_id: str) -> str:
    """Reads a specific secret version or staged value from Google Secret Manager.

    Args:
        secret_id: The ID of the secret.
        version_id: The version of the secret to access (e.g., '1', 'latest', 'AWESOME_BETA').

    Returns:
        The payload of the specified secret version.
    """
    client = SecretManagerClient()
    secret_payload = client.access_secret_version(secret_id, version_id)
    return secret_payload
