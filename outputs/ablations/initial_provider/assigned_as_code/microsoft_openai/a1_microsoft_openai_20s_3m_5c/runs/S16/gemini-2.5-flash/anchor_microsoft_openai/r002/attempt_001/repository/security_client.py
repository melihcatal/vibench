from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
from typing import Optional, Dict

class AzureKeyVaultSecurityClient:
    def __init__(self, vault_url: Optional[str] = None):
        if not vault_url:
            self.vault_url = os.environ.get("AZURE_KEYVAULT_VAULT_URL")
            if not self.vault_url:
                raise ValueError("Azure Key Vault URL not provided and AZURE_KEYVAULT_VAULT_URL environment variable is not set.")
        else:
            self.vault_url = vault_url
        
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)

    def get_secret(self, secret_id: str, version: Optional[str] = None) -> str:
        if version:
            secret = self.client.get_secret(secret_id, version=version)
        else:
            secret = self.client.get_secret(secret_id)
        return secret.value

    def set_secret(self, secret_id: str, secret_value: str, tags: Optional[Dict[str, str]] = None) -> str:
        secret = self.client.set_secret(secret_id, secret_value, tags=tags)
        return secret.id

    def get_secret_properties(self, secret_id: str):
        return self.client.get_secret(secret_id).properties

    def list_properties_of_secrets(self):
        return self.client.list_properties_of_secrets()
