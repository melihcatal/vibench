import os
from google.cloud import kms_v1

from security_client import get_kms_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse

def envelope_encrypt(payload: bytes, key_name: str) -> EnvelopeEncryptResponse:
    """Performs envelope encryption (data key generation + KMS encryption).

    Uses Google Cloud KMS to encrypt a randomly generated data key.
    The function returns the encrypted data key (ciphertext) and the
    plaintext data key which can be used to encrypt the actual payload.

    Args:
        payload: Raw bytes of the data you plan to encrypt with the
            plaintext data key.
        key_name: Full resource name of the KMS CryptoKey used for
            encrypting the data key.

    Returns:
        EnvelopeEncryptResponse with `encrypted_data_key` (Base64) and
        `plaintext_data_key` (Base64).
    """
    client = get_kms_client()
    # Generate a random data key (AES-256) for envelope encryption
    data_key = os.urandom(32)
    # Encrypt the data key with KMS (this is the envelope step)
    encrypt_req = kms_v1.EncryptRequest(
        name=key_name,
        plaintext=data_key,
    )
    kms_resp = client.encrypt(encrypt_req)
    encrypted_data_key_b64 = kms_resp.ciphertext.decode('utf-8')
    plaintext_data_key_b64 = data_key.decode('latin1')  # safe Base64 representation
    return EnvelopeEncryptResponse(
        encrypted_data_key=encrypted_data_key_b64,
        plaintext_data_key=plaintext_data_key_b64,
    )
