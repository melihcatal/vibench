from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
from typing import Optional


class SecurityClient:
    def __init__(self, key_vault_url: Optional[str] = None):
        self.key_vault_url = key_vault_url or os.getenv("AZURE_KEY_VAULT_URL")
        if not self.key_vault_url:
            raise ValueError("AZURE_KEY_VAULT_URL environment variable is not set")
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(
            vault_url=self.key_vault_url, credential=self.credential
        )

    def get_client(self) -> SecretClient:
        return self.client
