import os
import hvac

def read_vault_secret_version(secret_path: str, version: int) -> dict:
    vault_addr = os.getenv("VAULT_ADDR")
    vault_token = os.getenv("VAULT_TOKEN")
    vault_mount_point = os.getenv("VAULT_MOUNT_POINT", "secret")

    if not vault_addr or not vault_token:
        raise ValueError("VAULT_ADDR and VAULT_TOKEN environment variables must be set.")

    client = hvac.Client(url=vault_addr, token=vault_token)

    if not client.is_authenticated():
        raise ConnectionRefusedError("Vault client not authenticated.")

    try:
        # Assuming KV V2 secret engine
        read_response = client.secrets.kv.v2.read_secret_version(
            mount_point=vault_mount_point,
            path=secret_path,
            version=version
        )
        if read_response and 'data' in read_response and 'data' in read_response['data']:
            return read_response['data']['data']
        raise ValueError(f"Secret data not found for path '{secret_path}' version '{version}'.")
    except hvac.exceptions.InvalidPath as e:
        raise ValueError(f"Invalid Vault path or secret not found: {e}")
    except Exception as e:
        raise RuntimeError(f"Error reading secret '{secret_path}' version '{version}' from Vault: {e}")
