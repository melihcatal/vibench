import os
from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
key_client = KeyClient(vault_url=f'https://{key_vault_name}.vault.azure.net/', credential=DefaultAzureCredential())

def sign_or_verify_key(data):
    key_name = 'myKey'
    key_version = 'myVersion'
    result = key_client.sign(key_name, key_version, data)
    return result.result
