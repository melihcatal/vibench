from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

def sign_or_verify_key(key_name, data):
    credential = DefaultAzureCredential()
    client = KeyClient(vault_url="https://<your-key-vault-name>.vault.azure.net/", credential=credential)
    key = client.get_key(key_name)
    signed_data = client.sign(key, data)
    return signed_data.result()