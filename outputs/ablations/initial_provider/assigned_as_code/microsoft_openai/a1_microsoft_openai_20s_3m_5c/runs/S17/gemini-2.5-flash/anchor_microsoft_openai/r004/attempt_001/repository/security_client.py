from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient

def get_key_vault_cryptography_client(key_id: str) -> CryptographyClient:
    credential = DefaultAzureCredential()
    return CryptographyClient(key_id, credential=credential)
