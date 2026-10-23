import os

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def fetch_api_key() -> str:
    vault_url = os.environ["AZURE_KEY_VAULT_URL"]
    secret_name = os.getenv("API_KEY_SECRET_NAME", "api-key")
    client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
    return client.get_secret(secret_name).value
