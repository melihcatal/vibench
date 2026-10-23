from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

def fetch_api_key(secret_name: str) -> str:
    """
    Fetches an API key from Azure Key Vault.
    """
    key_vault_name = os.environ["KEY_VAULT_NAME"]
    kv_uri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=kv_uri, credential=credential)
    
    try:
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve secret '{secret_name}' from Azure Key Vault: {e}")

if __name__ == '__main__':
    # Example usage (requires KEY_VAULT_NAME and the secret to exist in Azure Key Vault)
    # Set environment variable KEY_VAULT_NAME before running
    # print(fetch_api_key("my-api-key"))
    pass
