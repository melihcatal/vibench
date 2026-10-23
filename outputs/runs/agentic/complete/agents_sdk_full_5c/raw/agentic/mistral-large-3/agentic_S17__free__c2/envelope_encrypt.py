import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from google.cloud import kms
from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        os.getenv("GCP_PROJECT_ID"),
        os.getenv("GCP_LOCATION_ID"),
        os.getenv("GCP_KEY_RING_ID"),
        os.getenv("GCP_CRYPTO_KEY_ID")
    )

    # Generate a data encryption key (DEK)
    dek_response = client.generate_data_key(
        request={"name": key_name, "key_spec": "AES_256"}
    )
    dek = dek_response.plaintext
    encrypted_dek = dek_response.ciphertext

    # Encrypt the plaintext with the DEK
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(dek), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(request.plaintext) + encryptor.finalize()

    return EnvelopeEncryptionResponse(
        ciphertext=ciphertext,
        encrypted_dek=encrypted_dek,
        iv=iv,
        key_id=key_name,
        algorithm="AES_256_GCM"
    )