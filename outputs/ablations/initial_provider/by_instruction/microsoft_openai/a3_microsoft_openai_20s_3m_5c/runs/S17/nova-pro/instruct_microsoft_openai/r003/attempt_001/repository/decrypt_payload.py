from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

key_vault_name = "your-key-vault-name"
key_name = "your-key-name"

def decrypt_payload(ciphertext):
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=f"https://{key_vault_name}.vault.azure.net/", credential=credential)
    key = key_client.get_key(key_name)
    decrypted_data = key_client.decrypt(key, ciphertext)
    return decrypted_data.result

if __name__ == "__main__":
    ciphertext = b'your-ciphertext'
    decrypted = decrypt_payload(ciphertext)
    print(decrypted.decode('utf-8'))