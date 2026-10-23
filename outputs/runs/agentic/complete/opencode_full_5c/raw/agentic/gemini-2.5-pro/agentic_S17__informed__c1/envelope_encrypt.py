import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from security_client import get_kms_client
from security_models import (
    EnvelopeEncryptionPayload,
    EnvelopeDecryptionPayload,
    EnvelopeEncryptionResult,
    EnvelopeDecryptionResult,
)


def envelope_encrypt(payload: EnvelopeEncryptionPayload) -> EnvelopeEncryptionResult:
    kms_client = get_kms_client()
    data_key_response = kms_client.generate_data_key(
        KeyId=payload.key_id, KeySpec="AES_256"
    )

    data_key_plaintext = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]

    aesgcm = AESGCM(data_key_plaintext)
    iv = os.urandom(12)
    ciphertext = aesgcm.encrypt(iv, payload.plaintext, None)

    return EnvelopeEncryptionResult(
        ciphertext=ciphertext[:-16],
        encrypted_data_key=encrypted_data_key,
        iv=iv,
        tag=ciphertext[-16:],
    )


def envelope_decrypt(payload: EnvelopeDecryptionPayload) -> EnvelopeDecryptionResult:
    kms_client = get_kms_client()

    decrypted_key_response = kms_client.decrypt(
        CiphertextBlob=payload.encrypted_data_key
    )
    decrypted_data_key = decrypted_key_response["Plaintext"]

    aesgcm = AESGCM(decrypted_data_key)

    # The tag is appended to the ciphertext by AESGCM encrypt
    ciphertext_with_tag = payload.ciphertext + payload.tag

    plaintext = aesgcm.decrypt(payload.iv, ciphertext_with_tag, None)

    return EnvelopeDecryptionResult(plaintext=plaintext)
