from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

def encrypt_payload(key_name, plaintext):
    credential = DefaultAzureCredential()
    client = KeyClient(vault_url="https://<your-key-vault-name>.vault.azure.net/", credential=credential)
    key = client.get_key(key_name)
    encrypted_data = client.encrypt(key, plaintext)
    return encrypted_data.result()