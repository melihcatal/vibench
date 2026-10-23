from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

key_vault_name = "your-key-vault-name"
key_name = "your-key-name"

def envelope_encrypt(plaintext):
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=f"https://{key_vault_name}.vault.azure.net/", credential=credential)
    key = key_client.get_key(key_name)
    encrypted_data = key_client.encrypt(key, plaintext.encode('utf-8'))
    return encrypted_data.result

if __name__ == "__main__":
    plaintext = "Hello, World!"
    encrypted = envelope_encrypt(plaintext)
    print(encrypted)