from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os

def fetch_api_key(secret_name: str) -> str:
    """
    Fetches an API key from Azure Key Vault.
    """
    key_vault_name = os.environ["AZURE_KEY_VAULT_NAME"]
    kv_uri = f"https://{key_vault_name}.vault.azure.net"

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=kv_uri, credential=credential)

    try:
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        raise RuntimeError(f"Could not retrieve secret {secret_name} from Azure Key Vault: {e}")

