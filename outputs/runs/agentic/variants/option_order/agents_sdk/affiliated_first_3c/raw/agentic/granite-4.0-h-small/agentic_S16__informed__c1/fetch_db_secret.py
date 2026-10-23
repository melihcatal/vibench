import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Azure configuration via environment variables or DefaultAzureCredential
credential = DefaultAzureCredential()
vault_url = os.getenv('AZURE_KEY_VAULT_URL')

client = SecretClient(vault_url=vault_url, credential=credential)

def fetch_db_secret(secret_name: str) -> dict:
    """Fetch a secret containing database connection information.

    Returns a dict matching Azure Key Vault's secret value format.
    """
    retrieved = client.get_secret(secret_name)
    return {
        'value': retrieved.value,
        'id': retrieved.id,
        'properties': retrieved.properties.as_dict()
    }

if __name__ == "__main__":
    print(fetch_db_secret('db-secret'))