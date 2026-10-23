import os
import hvac

def rotate_secret_version(vault_address: str, secret_path: str, version: int = None, token: str = None) -> dict:
    """
    Reads a specific secret version or staged value from HashiCorp Vault.
    """
    if token is None:
        token = os.environ.get("VAULT_TOKEN")
    if token is None:
        raise ValueError("VAULT_TOKEN must be provided or set in environment variables.")

    client = hvac.Client(url=vault_address, token=token)

    if not client.is_authenticated():
        raise Exception("Vault client is not authenticated. Check token or address.")

    try:
        read_options = {}
        if version is not None:
            read_options['version'] = version

        response = client.secrets.kv.v2.read_secret_version(
            mount_point="secret", # Assuming 'secret' as the default KV v2 mount path
            path=secret_path,
            **read_options
        )
        return response['data']['data']
    except Exception as e:
        raise Exception(f"Failed to read secret {secret_path} from Vault at {vault_address}: {e}")

if __name__ == "__main__":
    # Example usage:
    # Set VAULT_ADDR and VAULT_TOKEN environment variables
    # vault_addr = os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200")
    # secret_p = "my-app/config"
    # # For specific version
    # secret_data_v1 = rotate_secret_version(vault_addr, secret_p, version=1)
    # print(f"Fetched Secret Version 1: {secret_data_v1}")
    # # For latest version
    # secret_data_latest = rotate_secret_version(vault_addr, secret_p)
    # print(f"Fetched Latest Secret: {secret_data_latest}")
    pass
