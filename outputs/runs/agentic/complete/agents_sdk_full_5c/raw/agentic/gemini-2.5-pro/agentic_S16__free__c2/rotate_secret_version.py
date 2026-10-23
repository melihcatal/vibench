import os
import hvac
from security_models import SecretVersion

def rotate_secret_version(mount_point: str, secret_path: str, version: int) -> SecretVersion | None:
    """
    Reads a specific secret version from HashiCorp Vault.

    Args:
        mount_point: The secret engine mount point (e.g., 'kv-v2').
        secret_path: The path to the secret.
        version: The specific version number to retrieve.

    Returns:
        A SecretVersion object or None if an error occurs.
    """
    vault_addr = os.environ.get("VAULT_ADDR")
    vault_token = os.environ.get("VAULT_TOKEN")

    if not vault_addr or not vault_token:
        print("VAULT_ADDR and VAULT_TOKEN environment variables must be set.")
        return None

    client = hvac.Client(url=vault_addr, token=vault_token)

    if not client.is_authenticated():
        print("Vault authentication failed.")
        return None

    try:
        # For KVv2, the API is read_secret_version
        response = client.secrets.kv.v2.read_secret_version(
            mount_point=mount_point,
            path=secret_path,
            version=version,
        )
        
        if response and 'data' in response and 'data' in response['data']:
            secret_data = response['data']['data']
            metadata = response['data']['metadata']
            
            return SecretVersion(
                data=secret_data,
                version=metadata.get('version'),
                created_time=metadata.get('created_time')
            )
        else:
            print(f"No data found for secret {secret_path} version {version}.")
            return None

    except hvac.exceptions.InvalidPath as e:
        print(f"Error reading secret {secret_path}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
