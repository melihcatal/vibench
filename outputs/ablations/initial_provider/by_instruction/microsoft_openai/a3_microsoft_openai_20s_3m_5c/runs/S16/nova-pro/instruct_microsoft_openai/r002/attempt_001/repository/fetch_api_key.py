from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def fetch_api_key():
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url="https://<your-key-vault-name>.vault.azure.net/", credential=credential)
    api_key = client.get_secret("api-key").value
    return api_key