from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential
from base64 import b64encode

def encrypt_payload(key_vault_url: str, key_name: str, plaintext: str) -> str:
    """
    Encrypts a plaintext payload using a specified key in Azure Key Vault.
    """
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=key_vault_url, credential=credential)

    # Convert plaintext to bytes
    plaintext_bytes = plaintext.encode('utf-8')

    # Encrypt the payload with the specified key
    # Using 'A256CBC' algorithm, which is a symmetric encryption algorithm.
    # The actual key material is managed by Azure Key Vault.
    # The encrypt operation on a symmetric key in Azure Key Vault takes bytes and returns an EncryptResult.
    encrypt_result = key_client.encrypt(key_name=key_name, algorithm='A256CBC', plaintext=plaintext_bytes)
    
    # The ciphertext is in bytes, convert to base64 string for easier handling
    ciphertext = b64encode(encrypt_result.ciphertext).decode('utf-8')
    return ciphertext
