from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import json


class AzureJSONSecretParser:
    def __init__(self):
        self.key_vault_url = os.getenv("AZURE_KEY_VAULT_URL")
        if not self.key_vault_url:
            raise ValueError("AZURE_KEY_VAULT_URL environment variable is not set")
        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.key_vault_url, credential=credential)

    def parse_json_secret(self, secret_name: str) -> dict:
        secret = self.client.get_secret(secret_name)
        return json.loads(secret.value)
