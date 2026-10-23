from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

class SecretManagementClient:
    def __init__(self, vault_url: str = None):
        if vault_url is None:
            vault_url = os.environ.get("KEY_VAULT_URL")
            if not vault_url:
                raise ValueError("Key Vault URL must be provided or set in KEY_VAULT_URL environment variable.")
        self.vault_url = vault_url
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)

    def get_secret(self, secret_id: str) -> str:
        secret = self.client.get_secret(secret_id)
        return secret.value

    def get_secret_properties(self, secret_id: str):
        return self.client.get_secret_properties(secret_id)

    def list_properties_of_secrets(self):
        return self.client.list_properties_of_secrets()

    def set_secret(self, secret_id: str, value: str):
        return self.client.set_secret(secret_id, value)

    def update_secret_properties(self, secret_id: str, tags=None, content_type=None, enabled=None, expires_on=None, not_before=None):
        return self.client.update_secret_properties(secret_id, tags=tags, content_type=content_type, enabled=enabled, expires_on=expires_on, not_before=not_before)

    def get_secret_version(self, secret_id: str, version: str) -> str:
        secret_version = self.client.get_secret(secret_id, version=version)
        return secret_version.value
