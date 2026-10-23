import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from google.cloud import kms_v1

from security_client import get_gcp_kms_client
from security_models import EnvelopeEncryptionPayload, EnvelopeDecryptionPayload


def envelope_encrypt_payload(payload: EnvelopeEncryptionPayload) -> tuple[bytes, bytes]:
    """
    Performs envelope encryption on a payload.

    A new data encryption key (DEK) is generated locally. The plaintext is
    encrypted with this DEK. The DEK is then encrypted (wrapped) by a key
    managed in Google Cloud KMS.

    Args:
        payload: The payload to encrypt.

    Returns:
        A tuple containing the wrapped DEK and the ciphertext.
    """
    dek = AESGCM.generate_key(bit_length=256)
    aes_gcm = AESGCM(dek)

    nonce = os.urandom(12)
    ciphertext = aes_gcm.encrypt(nonce, payload.plaintext, payload.associated_data)

    kms_client = get_gcp_kms_client()
    encrypt_request = kms_v1.EncryptRequest(name=payload.key_name, plaintext=dek)
    encrypt_response = kms_client.encrypt(request=encrypt_request)
    wrapped_dek = encrypt_response.ciphertext

    return wrapped_dek, nonce + ciphertext


def envelope_decrypt_payload(payload: EnvelopeDecryptionPayload) -> bytes:
    """
    Performs envelope decryption on a payload.

    The wrapped data encryption key (DEK) is decrypted (unwrapped) by a key
    managed in Google Cloud KMS. The resulting plaintext DEK is then used to
    decrypt the ciphertext.

    Args:
        payload: The payload to decrypt.

    Returns:
        The decrypted plaintext.
    """
    kms_client = get_gcp_kms_client()
    decrypt_request = kms_v1.DecryptRequest(
        name=payload.key_name, ciphertext=payload.wrapped_dek
    )
    decrypt_response = kms_client.decrypt(request=decrypt_request)
    dek = decrypt_response.plaintext

    aes_gcm = AESGCM(dek)

    nonce = payload.ciphertext[:12]
    actual_ciphertext = payload.ciphertext[12:]

    plaintext = aes_gcm.decrypt(nonce, actual_ciphertext, payload.associated_data)

    return plaintext
