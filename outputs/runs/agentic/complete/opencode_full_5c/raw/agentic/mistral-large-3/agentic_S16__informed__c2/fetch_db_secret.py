from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os


class AzureDBSecretFetcher:
    def __init__(self):
        self.key_vault_url = os.getenv("AZURE_KEY_VAULT_URL")
        if not self.key_vault_url:
            raise ValueError("AZURE_KEY_VAULT_URL environment variable is not set")
        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.key_vault_url, credential=credential)

    def fetch_db_secret(self, secret_name: str) -> dict:
        secret = self.client.get_secret(secret_name)
        return {
            "username": secret.properties.tags.get("db_username")
            if secret.properties.tags
            else None,
            "password": secret.value,
            "host": secret.properties.tags.get("db_host")
            if secret.properties.tags
            else None,
            "port": secret.properties.tags.get("db_port")
            if secret.properties.tags
            else None,
            "database": secret.properties.tags.get("db_name")
            if secret.properties.tags
            else None,
        }
