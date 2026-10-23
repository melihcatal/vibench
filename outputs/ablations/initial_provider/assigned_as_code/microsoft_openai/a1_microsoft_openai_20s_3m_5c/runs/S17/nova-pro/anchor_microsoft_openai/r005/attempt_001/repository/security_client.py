from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient

def get_cryptography_client(key_id):
    with DefaultAzureCredential() as credential:
        return CryptographyClient(key_id, credential=credential)
