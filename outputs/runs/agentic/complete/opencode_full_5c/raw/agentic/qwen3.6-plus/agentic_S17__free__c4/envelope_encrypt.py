import os
import base64
from typing import Optional, Dict
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

from security_client import SecurityClient, KMSConfig
from security_models import (
    EnvelopeEncryptionRequest,
    EnvelopeEncryptionResponse,
    DecryptionRequest,
    normalize_payload,
)

AWS_KMS_SERVICE_NAME = "kms"
AWS_KMS_ENDPOINT_HOST = "kms.{region}.amazonaws.com"
AES_GCM_NONCE_SIZE = 12
AES_GCM_TAG_SIZE = 16


def generate_nonce() -> bytes:
    return os.urandom(AES_GCM_NONCE_SIZE)


def aes_gcm_encrypt(plaintext: bytes, key: bytes) -> tuple:
    nonce = generate_nonce()
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(nonce),
        backend=default_backend(),
    ).encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag
    return nonce, ciphertext, tag


def aes_gcm_decrypt(nonce: bytes, ciphertext: bytes, tag: bytes, key: bytes) -> bytes:
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(nonce, tag),
        backend=default_backend(),
    ).decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext


def envelope_encrypt(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[KMSConfig] = None,
) -> EnvelopeEncryptionResponse:
    client = SecurityClient(config=config)
    normalized_plaintext = normalize_payload(plaintext)

    data_key_result = client.generate_data_key(
        key_id=key_id,
        key_spec="AES_256",
        encryption_context=client.normalize_encryption_context(encryption_context),
    )

    plaintext_data_key = data_key_result["plaintext_key"]
    encrypted_data_key = data_key_result["encrypted_key"]

    nonce, ciphertext, tag = aes_gcm_encrypt(normalized_plaintext, plaintext_data_key)

    combined_ciphertext = nonce + tag + ciphertext

    response = EnvelopeEncryptionResponse(
        encrypted_data_key=encrypted_data_key,
        ciphertext=combined_ciphertext,
        key_id=data_key_result["key_id"],
        encryption_algorithm="AES_256_GCM",
        data_key_spec=data_key_result.get("key_spec", "AES_256"),
        request_id="",
    )

    return response


def envelope_decrypt(
    encrypted_data_key: bytes,
    ciphertext: bytes,
    encryption_context: Optional[Dict[str, str]] = None,
    config: Optional[KMSConfig] = None,
) -> bytes:
    client = SecurityClient(config=config)

    decrypt_result = client.decrypt(
        DecryptionRequest(
            ciphertext_blob=encrypted_data_key,
            encryption_context=client.normalize_encryption_context(encryption_context),
        )
    )

    plaintext_data_key = decrypt_result.plaintext

    nonce = ciphertext[:AES_GCM_NONCE_SIZE]
    tag = ciphertext[AES_GCM_NONCE_SIZE : AES_GCM_NONCE_SIZE + AES_GCM_TAG_SIZE]
    actual_ciphertext = ciphertext[AES_GCM_NONCE_SIZE + AES_GCM_TAG_SIZE :]

    plaintext = aes_gcm_decrypt(nonce, actual_ciphertext, tag, plaintext_data_key)
    return plaintext


def envelope_encrypt_to_dict(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> dict:
    response = envelope_encrypt(plaintext, key_id, encryption_context)
    return response.to_dict()


def envelope_decrypt_from_dict(
    encrypted_data_key_b64: str,
    ciphertext_b64: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> str:
    encrypted_data_key = base64.b64decode(encrypted_data_key_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = envelope_decrypt(encrypted_data_key, ciphertext, encryption_context)
    return plaintext.decode("utf-8")
