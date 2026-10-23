import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from google.cloud import kms
from security_client import get_kms_client, KMSConfig
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        KMSConfig.project_id, KMSConfig.location_id, KMSConfig.key_ring_id, KMSConfig.key_id
    )

    # Generate a data encryption key (DEK)
    dek_response = client.generate_data_key(
        request={"name": key_name, "key_spec": "AES_256"}
    )
    dek = dek_response.plaintext
    encrypted_dek = dek_response.ciphertext

    # Encrypt the plaintext with the DEK
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(dek), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    pad_length = 16 - (len(request.plaintext) % 16)
    padded_plaintext = request.plaintext + bytes([pad_length] * pad_length)
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    return EnvelopeEncryptionResponse(
        ciphertext=ciphertext,
        encrypted_dek=encrypted_dek,
        iv=iv,
        algorithm="AES_256_CBC"
    )