import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from security_client import get_gcp_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse

def envelope_encrypt_gcp(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    """
    Performs envelope encryption using Google Cloud KMS to create and wrap a data key.
    """
    kms_client = get_gcp_kms_client()
    key_path = request.key_id

    # Generate a local data encryption key (DEK)
    dek = os.urandom(32) # AES-256

    # Encrypt the DEK with the GCP KMS Customer Master Key (CMK)
    try:
        encrypt_response = kms_client.encrypt(
            name=key_path,
            plaintext=dek,
        )
        encrypted_dek = encrypt_response.ciphertext
    except Exception as e:
        return EnvelopeEncryptionResponse(ciphertext=b'', encrypted_data_key=b'', success=False, error=str(e))

    # Encrypt the plaintext data with the local DEK
    iv = os.urandom(12) # GCM standard nonce size
    cipher = Cipher(algorithms.AES(dek), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(request.plaintext) + encryptor.finalize()

    # The final ciphertext blob contains the IV and GCM tag
    final_payload = iv + encryptor.tag + ciphertext

    return EnvelopeEncryptionResponse(
        ciphertext=final_payload,
        encrypted_data_key=encrypted_dek,
        success=True
    )
