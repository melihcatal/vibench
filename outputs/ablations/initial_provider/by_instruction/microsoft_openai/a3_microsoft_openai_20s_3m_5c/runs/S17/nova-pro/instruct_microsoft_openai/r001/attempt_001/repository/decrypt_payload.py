from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

key_vault_name = "your-key-vault-name"
key_name = "your-key-name"

def decrypt_payload(ciphertext: str) -> str:
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=f"https://{key_vault_name}.vault.azure.net/", credential=credential)
    key = key_client.get_key(key_name)
    decrypted_data = key_client.decrypt(key, ciphertext)
    return decrypted_data.result.decode('utf-8')