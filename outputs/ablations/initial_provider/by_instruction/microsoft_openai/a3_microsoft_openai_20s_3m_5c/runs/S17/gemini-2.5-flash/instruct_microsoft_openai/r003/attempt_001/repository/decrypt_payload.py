from security_client import SecurityClient
from security_models import DecryptionRequest, DecryptionResponse
import base64

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    """Decrypts a ciphertext payload with a managed key using Azure Key Vault."""
    security_client = SecurityClient(request.key_vault_url)
    crypto_client = security_client.get_cryptography_client(request.key_name)

    # Convert base64 ciphertext back to bytes
    ciphertext_bytes = base64.b64decode(request.ciphertext)

    # Decrypt the data using the specified key in Azure Key Vault
    # The algorithm should match the one used during encryption, e.g., 'RSA-OAEP'
    decrypt_result = crypto_client.decrypt('RSA-OAEP', ciphertext_bytes)

    # Convert decrypted bytes back to string
    plaintext = decrypt_result.plaintext.decode('utf-8')

    return DecryptionResponse(
        plaintext=plaintext
    )

