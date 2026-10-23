import os
import json
from security_client import SecretsManagerClient


def rotate_secret_version(secret_name: str, version: str) -> dict:
    """Reads a specific secret version or staged value.

    Args:
        secret_name: Name of the secret to rotate.
        version: Version ID or 'staged' to retrieve staged value.

    Returns:
        Fetched secret data for the requested version.
    """
    client = SecretsManagerClient()
    response = client.get_secret_version(name=secret_name, version=version)
    return response["SecretString"]


if __name__ == "__main__":
    # Example usage
    version_data = rotate_secret_version(
        os.getenv("SECRET_NAME"), os.getenv("VERSION_ID") or "staged"
    )
    print(f"Rotated secret version data: {version_data}")
