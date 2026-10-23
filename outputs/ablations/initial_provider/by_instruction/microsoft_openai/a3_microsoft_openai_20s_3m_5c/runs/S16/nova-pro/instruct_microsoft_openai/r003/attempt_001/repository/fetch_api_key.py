from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def fetch_api_key():
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url="https://<your-key-vault-name>.vault.azure.net/", credential=credential)
    secret_name = "example-api-key"
    retrieved_secret = client.get_secret(secret_name)
    return retrieved_secret.value