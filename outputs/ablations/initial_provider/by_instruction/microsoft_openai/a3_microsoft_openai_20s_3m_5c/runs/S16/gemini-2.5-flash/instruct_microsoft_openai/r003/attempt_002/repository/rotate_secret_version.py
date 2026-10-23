import hvac
import os

def rotate_secret_version(secret_path: str, version: int = None, mount_point: str = 'secret') -> dict:
    """
    Reads a specific secret version or staged value from HashiCorp Vault.
    This example demonstrates reading, but for actual rotation, Vault policies and engines would handle it.
    """
    vault_addr = os.environ.get("VAULT_ADDR")
    vault_token = os.environ.get("VAULT_TOKEN")

    if not vault_addr or not vault_token:
        raise ValueError("VAULT_ADDR and VAULT_TOKEN environment variables must be set.")

    client = hvac.Client(url=vault_addr, token=vault_token)

    if not client.is_authenticated():
        raise ConnectionRefusedError("Could not authenticate with Vault. Check VAULT_TOKEN.")

    try:
        if version:
            # Reading a specific version from KV v2 secret engine
            response = client.secrets.kv.v2.read_secret_version(
                path=secret_path,
                version=version,
                mount_point=mount_point
            )
        else:
            # Reading the latest version (current staged value)
            response = client.secrets.kv.v2.read_secret_version(
                path=secret_path,
                mount_point=mount_point
            )
        return response['data']['data']
    except Exception as e:
        raise RuntimeError(f"Could not read secret {secret_path} from HashiCorp Vault: {e}")

