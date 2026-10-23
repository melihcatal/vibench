from security_client import SecurityClient
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse
from cryptography.fernet import Fernet
import base64

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    """Implements envelope encryption using Azure Key Vault to wrap a data encryption key."""
    security_client = SecurityClient(request.key_vault_url)
    crypto_client = security_client.get_cryptography_client(request.key_name)

    # 1. Generate a symmetric data encryption key (DEK)
    data_encryption_key = Fernet.generate_key()
    f = Fernet(data_encryption_key)

    # 2. Encrypt the plaintext payload with the DEK
    ciphertext = f.encrypt(request.plaintext.encode('utf-8'))

    # 3. Encrypt the DEK with the KEK from Azure Key Vault (Key Wrapping)
    # The algorithm 'RSA-OAEP' is used for key wrapping/unwrapping with an asymmetric key
    wrap_result = crypto_client.wrap_key('RSA-OAEP', data_encryption_key)

    return EnvelopeEncryptionResponse(
        encrypted_data_key=base64.b64encode(wrap_result.encrypted_key).decode('utf-8'),
        ciphertext=base64.b64encode(ciphertext).decode('utf-8'),
        key_id=wrap_result.key_id,
        algorithm=wrap_result.algorithm
    )

