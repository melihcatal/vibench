import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient

key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
key_vault_url = f'https://{key_vault_name}.vault.azure.net/'
credential = DefaultAzureCredential()
key_client = KeyClient(vault_url=key_vault_url, credential=credential)

def decrypt_payload(ciphertext):
    key_name = 'myKey'
    key = key_client.get_key(key_name)
    decrypted_data = key_client.decrypt(key, ciphertext)
    return decrypted_data.result
