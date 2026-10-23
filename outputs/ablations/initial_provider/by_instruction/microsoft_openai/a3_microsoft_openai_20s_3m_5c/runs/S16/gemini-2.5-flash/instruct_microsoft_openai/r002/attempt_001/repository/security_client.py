from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from security_models import Secret
import os

class SecurityClient:
    def __init__(self):
        keyvault_uri = os.environ.get("AZURE_KEYVAULT_URI")
        if not keyvault_uri:
            raise ValueError("AZURE_KEYVAULT_URI environment variable not set.")
        self.client = SecretClient(vault_url=keyvault_uri, credential=DefaultAzureCredential())

    def get_secret(self, secret_name: str) -> Secret:
        azure_secret = self.client.get_secret(secret_name)
        return Secret(
            name=azure_secret.name,
            value=azure_secret.value,
            content_type=azure_secret.properties.content_type if azure_secret.properties.content_type else "text/plain",
            tags=azure_secret.properties.tags
        )

    def set_secret(self, secret: Secret) -> Secret:
        azure_secret = self.client.set_secret(
            name=secret.name,
            value=secret.value,
            content_type=secret.content_type,
            tags=secret.tags
        )
        return Secret(
            name=azure_secret.name,
            value=azure_secret.value,
            content_type=azure_secret.properties.content_type if azure_secret.properties.content_type else "text/plain",
            tags=azure_secret.properties.tags
        )

    def get_secret_with_version(self, secret_name: str, version: str) -> Secret:
        azure_secret = self.client.get_secret(secret_name, version=version)
        return Secret(
            name=azure_secret.name,
            value=azure_secret.value,
            content_type=azure_secret.properties.content_type if azure_secret.properties.content_type else "text/plain",
            tags=azure_secret.properties.tags
        )
