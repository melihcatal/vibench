import os
from azure.identity import DefaultAzureCredential
from typing import Optional, Dict
from azure.keyvault.secrets import SecretClient
from security_models import Secret

class SecurityClient:
    def __init__(self):
        keyvault_uri = os.environ.get("AZURE_KEYVAULT_URI")
        if not keyvault_uri:
            raise ValueError("AZURE_KEYVAULT_URI environment variable not set.")
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=keyvault_uri, credential=self.credential)

    def get_secret(self, secret_name: str, version: Optional[str] = None) -> Secret:
        if version:
            keyvault_secret = self.client.get_secret(secret_name, version=version)
        else:
            keyvault_secret = self.client.get_secret(secret_name)
        return Secret(
            name=keyvault_secret.name,
            value=keyvault_secret.value,
            content_type=keyvault_secret.properties.content_type,
            tags=keyvault_secret.properties.tags
        )

    def list_secrets(self):
        return self.client.list_properties_of_secrets()

    def set_secret(self, secret_name: str, secret_value: str, content_type: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
        self.client.set_secret(secret_name, secret_value, content_type=content_type, tags=tags)

    def update_secret_properties(self, secret_name: str, tags: Optional[Dict[str, str]] = None):
        secret_properties = self.client.get_secret(secret_name).properties
        secret_properties.tags = tags
        self.client.update_secret_properties(secret_properties)
