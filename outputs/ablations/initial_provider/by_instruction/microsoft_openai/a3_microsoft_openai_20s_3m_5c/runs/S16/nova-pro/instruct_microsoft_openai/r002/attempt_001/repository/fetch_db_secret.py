from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def fetch_db_secret():
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url="https://<your-key-vault-name>.vault.azure.net/", credential=credential)
    db_secret = client.get_secret("db-secret").value
    return db_secret