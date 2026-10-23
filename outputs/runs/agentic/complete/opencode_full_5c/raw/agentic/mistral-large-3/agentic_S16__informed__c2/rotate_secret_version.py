from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os


class AzureSecretVersionRotator:
    def __init__(self):
        self.key_vault_url = os.getenv("AZURE_KEY_VAULT_URL")
        if not self.key_vault_url:
            raise ValueError("AZURE_KEY_VAULT_URL environment variable is not set")
        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.key_vault_url, credential=credential)

    def rotate_secret_version(self, secret_name: str, version: str = None) -> str:
        if version:
            secret = self.client.get_secret_version(secret_name, version)
        else:
            secret = self.client.get_secret(secret_name)
        return secret.value
