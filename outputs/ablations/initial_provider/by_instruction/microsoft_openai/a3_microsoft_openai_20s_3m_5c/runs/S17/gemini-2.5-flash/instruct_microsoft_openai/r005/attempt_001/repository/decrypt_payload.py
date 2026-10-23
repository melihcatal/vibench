from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential
from base64 import b64decode

def decrypt_payload(key_vault_url: str, key_name: str, ciphertext: str) -> str:
    """
    Decrypts a ciphertext payload using a specified key in Azure Key Vault.
    """
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=key_vault_url, credential=credential)

    # Convert base64 ciphertext to bytes
    ciphertext_bytes = b64decode(ciphertext.encode('utf-8'))

    # Decrypt the payload with the specified key. The algorithm must match the encryption algorithm.
    decrypt_result = key_client.decrypt(key_name=key_name, algorithm='A256CBC', ciphertext=ciphertext_bytes)
    
    # The plaintext is in bytes, convert to utf-8 string
    plaintext = decrypt_result.plaintext.decode('utf-8')
    return plaintext
