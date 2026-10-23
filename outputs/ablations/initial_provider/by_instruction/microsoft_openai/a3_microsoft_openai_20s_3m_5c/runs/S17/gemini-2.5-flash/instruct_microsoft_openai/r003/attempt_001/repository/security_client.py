from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient
from openai import AzureOpenAI
import os

class SecurityClient:
    def __init__(self, key_vault_url: str):
        self.key_vault_url = key_vault_url
        self.credential = DefaultAzureCredential()
        self.key_client = KeyClient(vault_url=self.key_vault_url, credential=self.credential)

    def get_cryptography_client(self, key_name: str):
        key = self.key_client.get_key(key_name)
        return CryptographyClient(key, self.credential)

    def get_openai_client(self):
        return AzureOpenAI(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            api_version="2023-05-15",
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
        )
