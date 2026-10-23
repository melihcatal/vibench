import os
import hvac
from security_client import get_hvac_client

def read_specific_secret_version(mount_point: str, path: str, version: int) -> dict | None:
    """
    Reads a specific version of a secret from HashiCorp Vault.

    Args:
        mount_point: The mount point of the KVv2 secrets engine.
        path: The path to the secret.
        version: The specific version number to retrieve.

    Returns:
        The secret data as a dictionary, or None if an error occurs.
    """
    try:
        client = get_hvac_client()

        if not client:
            print("Vault client is not authenticated.")
            return None

        # The read_secret_version method is used for KVv2
        response = client.secrets.kv.v2.read_secret_version(
            mount_point=mount_point,
            path=path,
            version=version,
        )

        return response['data']['data']

    except hvac.exceptions.InvalidPath:
        print(f"Error: Secret path '{path}' not found at mount point '{mount_point}'.")
        return None
    except hvac.exceptions.Forbidden:
        print("Error: Permission denied. Check Vault policies.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Example usage would be in a different file.
# if __name__ == "__main__":
#     secret_path = os.environ.get("VAULT_SECRET_PATH")
#     secret_version_str = os.environ.get("VAULT_SECRET_VERSION")
#     kv_mount_point = os.environ.get("VAULT_KV_MOUNT_POINT", "secret")

#     if secret_path and secret_version_str:
#         try:
#             secret_version = int(secret_version_str)
#             secret_data = read_specific_secret_version(
#                 mount_point=kv_mount_point,
#                 path=secret_path,
#                 version=secret_version
#             )
#             if secret_data:
#                 print(f"Successfully read version {secret_version} of '{secret_path}'.")
#                 print(f"Secret keys: {list(secret_data.keys())}")
#             else:
#                 print("Failed to read secret version.")
#         except ValueError:
#             print("VAULT_SECRET_VERSION must be an integer.")
#     else:
#         print("Please set VAULT_SECRET_PATH and VAULT_SECRET_VERSION environment variables.")
