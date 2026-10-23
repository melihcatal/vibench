from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os


class AzureKeyVaultClient:
    def __init__(self):
        self.key_vault_url = os.getenv("AZURE_KEY_VAULT_URL")
        self.client = SecretClient(
            vault_url=self.key_vault_url, credential=DefaultAzureCredential()
        )

    def fetch_db_secret(self, secret_name: str) -> str:
        retrieved_secret = self.client.get_secret(secret_name)
        return retrieved_secret.value
