import os
import hvac

def read_vault_secret_version(secret_path: str, version: int = None, mount_point: str = 'secret') -> dict:
    """Reads a specific version or latest value of a secret from HashiCorp Vault (HCP Vault via HVAC client)."""
    vault_addr = os.environ.get("VAULT_ADDR")
    vault_token = os.environ.get("VAULT_TOKEN")

    if not vault_addr or not vault_token:
        raise ValueError("VAULT_ADDR and VAULT_TOKEN environment variables must be set.")

    client = hvac.Client(url=vault_addr, token=vault_token)

    if not client.is_authenticated():
        raise ConnectionError("Failed to authenticate with HashiCorp Vault.")

    try:
        if version is None:
            # Read latest version of KV version 2 secret
            read_response = client.secrets.kv.v2.read_secret_version(
                path=secret_path,
                mount_point=mount_point
            )
        else:
            # Read specific version of KV version 2 secret
            read_response = client.secrets.kv.v2.read_secret_version(
                path=secret_path,
                version=version,
                mount_point=mount_point
            )
        return read_response['data']['data']
    except hvac.exceptions.VaultError as e:
        raise ValueError(f"Error reading secret '{secret_path}' version '{version or 'latest'}' from Vault: {e}") from e
