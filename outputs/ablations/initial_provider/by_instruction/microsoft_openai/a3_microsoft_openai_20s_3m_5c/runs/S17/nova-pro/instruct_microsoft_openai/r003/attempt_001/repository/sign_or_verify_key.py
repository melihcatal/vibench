from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

key_vault_name = "your-key-vault-name"
key_name = "your-key-name"

def sign_or_verify_key(data):
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=f"https://{key_vault_name}.vault.azure.net/", credential=credential)
    key = key_client.get_key(key_name)
    signed_data = key_client.sign(key, data)
    return signed_data.result

if __name__ == "__main__":
    data = b'your-data'
    signed = sign_or_verify_key(data)
    print(signed)