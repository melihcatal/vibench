import os
from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
key_client = KeyClient(vault_url=f'https://{key_vault_name}.vault.azure.net/', credential=DefaultAzureCredential())

def encrypt_payload(plaintext):
    key_name = 'myKey'
    key_version = 'myVersion'
    result = key_client.encrypt(key_name, key_version, plaintext.encode('utf-8'))
    return result.ciphertext
