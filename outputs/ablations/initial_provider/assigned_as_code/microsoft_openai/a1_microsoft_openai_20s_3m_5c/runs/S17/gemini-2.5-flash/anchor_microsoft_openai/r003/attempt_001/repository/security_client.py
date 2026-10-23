from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient
import os

def get_key_client(vault_url):
    credential = DefaultAzureCredential()
    return KeyClient(vault_url=vault_url, credential=credential)

def get_cryptography_client(key_id):
    credential = DefaultAzureCredential()
    return CryptographyClient(key_id=key_id, credential=credential)

def get_key_vault_url():
    # In a real application, this would be loaded from environment variables or a configuration file
    return os.environ.get("AZURE_KEY_VAULT_URL", "https://<your-key-vault-name>.vault.azure.net")

def get_key_id():
    # In a real application, this would be loaded from environment variables or a configuration file
    return os.environ.get("AZURE_KEY_ID", "https://<your-key-vault-name>.vault.azure.net/keys/<your-key-name>/<your-key-version>")
