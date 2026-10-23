from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_secret_client(vault_url: str) -> SecretClient:
    """Initializes and returns an Azure Key Vault SecretClient."""
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)

def get_vault_url(config: dict) -> str:
    """Retrieves the Azure Key Vault URL from configuration."""
    if 'vault_url' not in config:
        raise ValueError("'vault_url' must be provided in the configuration.")
    return config['vault_url']
