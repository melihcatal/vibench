from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(
    vault_url="https://<your-key-vault-name>.vault.azure.net/", credential=credential
)


def fetch_api_key(secret_name):
    secret = client.get_secret(secret_name)
    return secret.value
