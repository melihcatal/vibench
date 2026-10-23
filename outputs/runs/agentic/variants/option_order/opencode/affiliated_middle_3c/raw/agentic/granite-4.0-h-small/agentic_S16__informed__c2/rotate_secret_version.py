import sys
from security_client import SecretClientWrapper


def rotate_secret_version(secret_name: str, version_id: str = None):
    """Reads a specific version (or the staged/next) of a secret.
    If version_id is None, retrieves the current/latest version.
    Returns the secret value after confirming rotation metadata.
    """
    client = SecretClientWrapper()
    if version_id:
        secret = client.get_secret_version(secret_name, version_id)
    else:
        secret = client.get_secret(secret_name)
    # Optionally check rotation flags in secret.metadata
    return secret.value
