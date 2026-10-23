import hvac
import os

def rotate_secret_version(secret_path: str, version: int = None) -> dict:
    """
    Reads a specific secret version from HashiCorp Vault. 
    (Note: Actual rotation typically involves writing a new version.)
    """
    vault_addr = os.environ.get("VAULT_ADDR")
    vault_token = os.environ.get("VAULT_TOKEN")

    if not vault_addr or not vault_token:
        raise ValueError("VAULT_ADDR and VAULT_TOKEN environment variables must be set.")

    client = hvac.Client(url=vault_addr, token=vault_token)

    if not client.is_authenticated():
        raise RuntimeError("Failed to authenticate with HashiCorp Vault. Check VAULT_TOKEN.")

    try:
        read_options = {"path": secret_path}
        if version is not None:
            read_options["version"] = version
        
        response = client.secrets.kv.read_secret_version(**read_options)
        return response['data']['data']
    except Exception as e:
        raise RuntimeError(f"Failed to read secret '{secret_path}' version {version if version else 'latest'} from HashiCorp Vault: {e}")

if __name__ == '__main__':
    # Example usage (requires VAULT_ADDR and VAULT_TOKEN environment variables)
    # Set VAULT_ADDR and VAULT_TOKEN before running
    # print(rotate_secret_version("secret/data/my-app/config", version=1))
    pass
