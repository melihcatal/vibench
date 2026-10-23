from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, KeyWrapAlgorithm
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse

def envelope_encrypt(request: EnvelopeEncryptionRequest, config=None) -> EnvelopeEncryptionResponse:
    config = config or {}
    # Generate a symmetric content encryption key (CEK) locally
    cek = os.urandom(32)  # 256-bit key
    iv = os.urandom(16)  # 128-bit IV for AES GCM

    # Encrypt the CEK with the master key in Azure Key Vault (wrap key operation)
    with DefaultAzureCredential() as credential:
        with CryptographyClient(request.key_id, credential=credential) as client:
            key_wrap_response = client.wrap_key(KeyWrapAlgorithm.rsa_oaep, cek)
            encrypted_data_key = key_wrap_response.encrypted_key

    # Encrypt the plaintext payload with the CEK locally using AES-256 GCM
    cipher = Cipher(algorithms.AES(cek), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(request.plaintext) + encryptor.finalize()
    tag = encryptor.tag

    return EnvelopeEncryptionResponse(
        encrypted_data_key=encrypted_data_key,
        ciphertext=ciphertext,
        iv=iv,
        tag=tag,
        key_id=request.key_id,
        algorithm="A256GCM"
    )
