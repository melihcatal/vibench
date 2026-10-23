from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from os import urandom

from security_client import get_key_vault_cryptography_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse

def envelope_encrypt(request: EnvelopeEncryptionRequest):
    # Generate a random data encryption key (DEK)
    data_encryption_key = urandom(32)  # 256-bit key
    iv = urandom(12)  # 96-bit IV for AES GCM

    # Encrypt the plaintext with the DEK locally using AES GCM
    cipher = Cipher(algorithms.AES(data_encryption_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(request.plaintext) + encryptor.finalize()
    tag = encryptor.tag

    # Use Azure Key Vault to wrap (encrypt) the DEK with the KEK
    key_vault_client = get_key_vault_cryptography_client(request.key_id)
    
    # Use AESA256 for wrapping as it's a common algorithm for key wrapping
    wrapped_key_response = key_vault_client.wrap_key(EncryptionAlgorithm.aes256, data_encryption_key)
    encrypted_dek = wrapped_key_response.encrypted_key

    return EnvelopeEncryptionResponse(
        ciphertext=ciphertext,
        encrypted_key=encrypted_dek,
        iv=iv,
        tag=tag,
        key_id=request.key_id,
        algorithm="AES256GCM_Envelope"
    )
