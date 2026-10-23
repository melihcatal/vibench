from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from .security_models import SecretInfo
import os
import json

class AzureKeyVaultSecurityClient:
    def __init__(self, vault_url: str = None):
        if vault_url is None:
            vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
            if not vault_url:
                raise ValueError("Azure Key Vault URL must be provided or set in AZURE_KEY_VAULT_URL environment variable.")
        self.vault_url = vault_url
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)

    def get_secret(self, secret_name: str) -> SecretInfo:
        secret = self.client.get_secret(secret_name)
        return SecretInfo(name=secret.name, value=secret.value, properties=secret.properties.as_dict())

    def get_secret_version(self, secret_name: str, version: str) -> SecretInfo:
        secret = self.client.get_secret(secret_name, version=version)
        return SecretInfo(name=secret.name, value=secret.value, properties=secret.properties.as_dict())

    def set_secret(self, secret_name: str, secret_value: str) -> SecretInfo:
        secret = self.client.set_secret(secret_name, secret_value)
        return SecretInfo(name=secret.name, value=secret.value, properties=secret.properties.as_dict())

    def get_secret_versions(self, secret_name: str):
        versions = []
        for secret_properties in self.client.list_properties_of_secret_versions(secret_name):
            versions.append(secret_properties)
        return versions

    def list_secrets(self):
        secrets = []
        for secret_properties in self.client.list_properties_of_secrets():
            secrets.append(secret_properties)
        return secrets
