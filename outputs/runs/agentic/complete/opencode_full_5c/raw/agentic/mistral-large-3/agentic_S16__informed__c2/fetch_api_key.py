from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os


class AzureSecretFetcher:
    def __init__(self):
        self.key_vault_url = os.getenv("AZURE_KEY_VAULT_URL")
        if not self.key_vault_url:
            raise ValueError("AZURE_KEY_VAULT_URL environment variable is not set")
        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.key_vault_url, credential=credential)

    def fetch_api_key(self, secret_name: str) -> str:
        secret = self.client.get_secret(secret_name)
        return secret.value
