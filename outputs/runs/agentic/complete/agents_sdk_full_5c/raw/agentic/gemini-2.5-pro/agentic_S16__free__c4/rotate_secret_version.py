import os
import hvac

def read_specific_secret_version(
    mount_point: str, 
    path: str, 
    version: int
) -> dict | None:
    """
    Reads a specific version of a secret from HashiCorp Vault.

    This is useful for rotation scenarios where you need to access a previous
    or pending version of a secret.

    Args:
        mount_point: The mount point of the KV secrets engine (e.g., 'kv-v2').
        path: The path to the secret.
        version: The specific version number to retrieve.

    Returns:
        A dictionary containing the secret data, or None on failure.
    """
    vault_addr = os.getenv("VAULT_ADDR")
    vault_token = os.getenv("VAULT_TOKEN")

    if not vault_addr or not vault_token:
        print("VAULT_ADDR and VAULT_TOKEN environment variables must be set.")
        return None

    try:
        client = hvac.Client(url=vault_addr, token=vault_token)
        
        if not client.is_authenticated():
            print("Vault authentication failed.")
            return None

        # read_secret_version returns the full response, data is in ['data']['data']
        response = client.secrets.kv.v2.read_secret_version(
            mount_point=mount_point,
            path=path,
            version=version,
        )
        
        return response['data']['data']
        
    except hvac.exceptions.InvalidPath:
        print(f"Secret not found at path: {path}")
        return None
    except hvac.exceptions.Forbidden:
        print(f"Permission denied for path: {path}")
        return None
    except Exception as e:
        print(f"An error occurred while communicating with Vault: {e}")
        return None

