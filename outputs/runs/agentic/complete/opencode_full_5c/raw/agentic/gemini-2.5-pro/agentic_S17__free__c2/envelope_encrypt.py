import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from security_client import get_gcp_kms_client
from security_models import EnvelopeEncryptionPayload


def envelope_encrypt_data(payload: EnvelopeEncryptionPayload) -> dict:
    dek = AESGCM.generate_key(bit_length=256)

    gcp_kms_client = get_gcp_kms_client()
    response = gcp_kms_client.encrypt(name=payload.key_path, plaintext=dek)
    encrypted_dek = response.ciphertext

    aes_gcm = AESGCM(dek)
    nonce = os.urandom(12)
    ciphertext = aes_gcm.encrypt(nonce, payload.plaintext, None)

    return {
        "encrypted_dek": encrypted_dek,
        "ciphertext": ciphertext,
        "nonce": nonce,
    }
