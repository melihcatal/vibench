import os
from security_client import SecretManagementClient


def rotate_secret_version(secret_name, version):
    """Read a specific secret version (or staged value) for a rotation operation.

    Args:
        secret_name (str): Name of the secret.
        version (str): Version identifier or 'staged'.

    Returns:
        dict: Secret fields for the requested version (provider: Google Secret Manager).
    """
    client = SecretManagementClient()
    response = client.get_secret_version(name=secret_name, version=version)
    # Provider: Google Secret Manager
    return response["data"]
