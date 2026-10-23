import os
from security_client import get_hashicorp_vault_client
from security_models import SecretItem

def rotate_secret_version(secret_path: str, mount_point: str = 'secret') -> SecretItem:
    vault_address = os.environ.get("VAULT_ADDR")
    vault_token = os.environ.get("VAULT_TOKEN")

    if not vault_address or not vault_token:
        raise ValueError("VAULT_ADDR and VAULT_TOKEN environment variables must be set.")

    client = get_hashicorp_vault_client(vault_address, vault_token)

    if not client.is_authenticated():
        raise ConnectionError("Failed to authenticate with HashiCorp Vault. Check VAULT_TOKEN.")

    try:
        # In a real scenario, this would trigger a rotation. HashiCorp Vault's API
        # for generic secrets usually involves writing a new version or deleting the old.
        # For specific secret engines (like databases), there are specific rotation endpoints.
        # This example simulates reading the *current* latest version after a conceptual rotation.
        read_response = client.read(path=f'{mount_point}/{secret_path}')
        if read_response and 'data' in read_response and 'data' in read_response['data']:
            secret_data = read_response['data']['data']
            # Assuming the secret content is a simple key-value for demonstration
            return SecretItem(
                name=secret_path,
                value=str(secret_data), # Convert dict to string for generic value storage
                metadata=read_response['data']['metadata']
            )
        else:
            raise ValueError(f"Secret data not found for path: {secret_path}")

    except Exception as e:
        raise RuntimeError(f"Failed to interact with HashiCorp Vault for secret rotation: {e}")
