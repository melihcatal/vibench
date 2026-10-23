from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

def decrypt_payload(key_name, ciphertext):
    credential = DefaultAzureCredential()
    client = KeyClient(vault_url="https://<your-key-vault-name>.vault.azure.net/", credential=credential)
    key = client.get_key(key_name)
    decrypted_data = client.decrypt(key, ciphertext)
    return decrypted_data.result()