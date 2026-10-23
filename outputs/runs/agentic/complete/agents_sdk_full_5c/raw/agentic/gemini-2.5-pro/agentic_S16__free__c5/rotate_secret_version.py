
import os
from security_client import get_vault_client

def read_secret_by_version(path: str, version: int) -> dict | None:
    """
    Reads a specific version of a secret from HashiCorp Vault.

    Args:
        path: The path to the secret in Vault.
        version: The specific version number to retrieve.

    Returns:
        The secret data as a dictionary, or None on failure.
    """
    try:
        client = get_vault_client()
        if not client:
            print("Vault client could not be initialized.")
            return None

        # This method is for KV v2 secrets engine
        secret_version_response = client.secrets.kv.v2.read_secret_version(
            path=path,
            version=version,
        )

        return secret_version_response['data']['data']

    except Exception as e:
        print(f"Error reading secret version from Vault: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Set VAULT_ADDR and VAULT_TOKEN environment variables.
    SECRET_PATH = os.environ.get("VAULT_SECRET_PATH", "kv/my-app/db")
    SECRET_VERSION = int(os.environ.get("VAULT_SECRET_VERSION", "1"))

    secret_data = read_secret_by_version(SECRET_PATH, SECRET_VERSION)

    if secret_data:
        print(f"Successfully read version {SECRET_VERSION} of secret at '{SECRET_PATH}'.")
        # In a real app, avoid printing secrets.
        # print("Secret data:", secret_data)
    else:
        print(f"Failed to read version {SECRET_VERSION} of secret at '{SECRET_PATH}'.")
