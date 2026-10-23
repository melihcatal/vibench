from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode

def envelope_encrypt(key_vault_url: str, master_key_name: str, plaintext: str) -> tuple[str, str]:
    """
    Implements envelope encryption using Azure Key Vault for the master key.
    Returns encrypted DEK and encrypted payload.
    """
    # 1. Generate a local data encryption key (DEK)
    dek = Fernet.generate_key()
    f = Fernet(dek)

    # 2. Encrypt the plaintext with the DEK
    encrypted_payload = f.encrypt(plaintext.encode('utf-8')).decode('utf-8')

    # 3. Encrypt the DEK using the master key in Azure Key Vault
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=key_vault_url, credential=credential)

    # Azure Key Vault encrypts bytes, so encode DEK to bytes first
    dek_bytes = dek
    encrypt_dek_result = key_client.encrypt(key_name=master_key_name, algorithm='RSA-OAEP', plaintext=dek_bytes)
    
    # The encrypted DEK is in bytes, convert to base64 string
    encrypted_dek = b64encode(encrypt_dek_result.ciphertext).decode('utf-8')

    return encrypted_dek, encrypted_payload
