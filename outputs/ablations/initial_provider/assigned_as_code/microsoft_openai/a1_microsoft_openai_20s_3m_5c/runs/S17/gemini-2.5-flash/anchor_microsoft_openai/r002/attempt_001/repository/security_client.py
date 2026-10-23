from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient
import os

class SecurityClient:
    def __init__(self, key_vault_url: str = None):
        if key_vault_url is None:
            self.key_vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
            if not self.key_vault_url:
                raise ValueError("AZURE_KEY_VAULT_URL environment variable not set.")
        else:
            self.key_vault_url = key_vault_url
        self.credential = DefaultAzureCredential()

    def get_key_client(self) -> KeyClient:
        return KeyClient(vault_url=self.key_vault_url, credential=self.credential)

    def get_cryptography_client(self, key_id: str) -> CryptographyClient:
        return CryptographyClient(key_id=key_id, credential=self.credential)
