from security_client import SecurityClient
from security_models import EncryptionRequest, EncryptionResponse
import base64
import os

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    """Encrypts a plaintext payload with a managed key using Azure Key Vault."""
    security_client = SecurityClient(request.key_vault_url)
    crypto_client = security_client.get_cryptography_client(request.key_name)

    # Convert plaintext to bytes
    plaintext_bytes = request.plaintext.encode('utf-8')

    # Encrypt the data using the specified key in Azure Key Vault
    # Using 'RSA-OAEP' as a common asymmetric encryption algorithm
    encrypt_result = crypto_client.encrypt('RSA-OAEP', plaintext_bytes)

    # The encrypted data (ciphertext) is in bytes, convert to base64 string for storage/transmission
    ciphertext_b64 = base64.b64encode(encrypt_result.ciphertext).decode('utf-8')

    return EncryptionResponse(
        ciphertext=ciphertext_b64,
        key_id=encrypt_result.key_id,
        algorithm=encrypt_result.algorithm
    )

