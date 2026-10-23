import os
import hvac

def read_vault_secret_version(
    secret_path: str,
    version: int = None,
    mount_point: str = 'secret',
    vault_addr: str = None,
    token: str = None
) -> dict:
    """
    Reads a specific secret version or staged value from HashiCorp Vault.
    """
    if vault_addr is None:
        vault_addr = os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200")
    if token is None:
        token = os.environ.get("VAULT_TOKEN")

    if not token:
        raise ValueError("VAULT_TOKEN environment variable or 'token' argument must be set.")

    client = hvac.Client(url=vault_addr, token=token)

    if not client.is_authenticated():
        raise RuntimeError(f"Failed to authenticate with Vault at {vault_addr}")

    try:
        read_options = {}
        if version is not None:
            read_options['version'] = version

        response = client.read(
            path=secret_path,
            mount_point=mount_point,
            **read_options
        )
        if response and 'data' in response and 'data' in response['data']:
            return response['data']['data']
        elif response and 'data' in response:
            # For non-KVv2 secrets, or if 'data' is directly under 'data'
            return response['data']
        else:
            return {}
    except hvac.exceptions.VaultError as e:
        raise RuntimeError(f"Error reading secret '{secret_path}' from Vault: {e}")

if __name__ == '__main__':
    # This is an example of how you might use it.
    # In a real scenario, VAULT_ADDR and VAULT_TOKEN would be set as environment variables.
    # SECRET_PATH = "my-app/config"
    # try:
    #     secret_data = read_vault_secret_version(SECRET_PATH, version=1)
    #     print(f"Fetched Vault Secret (version 1): {secret_data}")
    # except RuntimeError as e:
    #     print(f"Failed to read Vault secret: {e}")
    pass
