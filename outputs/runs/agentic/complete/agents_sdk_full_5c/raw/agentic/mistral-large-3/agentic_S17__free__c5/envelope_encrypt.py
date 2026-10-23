import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from google.cloud import kms
from security_client import get_kms_client, KMSConfig
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id, 
        request.location_id, 
        request.key_ring_id, 
        request.key_id
    )

    # Generate a data encryption key (DEK)
    dek_response = client.generate_data_key(
        request={
            "name": key_name,
            "key_spec": "AES_256"
        }
    )
    dek = dek_response.plaintext
    encrypted_dek = dek_response.ciphertext

    # Encrypt the plaintext with the DEK
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(request.plaintext) + padder.finalize()
    cipher = Cipher(algorithms.AES(dek), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return EnvelopeEncryptionResponse(
        ciphertext=ciphertext,
        encrypted_dek=encrypted_dek,
        iv=iv,
        provider="google-cloud-kms",
        model="projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
            request.project_id, request.location_id, request.key_ring_id, request.key_id
        )
    )