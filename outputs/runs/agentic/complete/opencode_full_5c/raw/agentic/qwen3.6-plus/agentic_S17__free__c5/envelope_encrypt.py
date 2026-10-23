import os
import struct
import hmac
import hashlib
from typing import Optional, Dict, Any

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend

from security_client import (
    SecurityClient,
    KMSClientConfig,
    DEFAULT_KEY_ID,
    DEFAULT_ENCRYPTION_CONTEXT,
)
from security_models import (
    GenerateDataKeyRequest,
    EncryptRequest,
    DecryptRequest,
    EnvelopeEncryptionResult,
    EnvelopeDecryptionResult,
    normalize_payload_to_bytes,
    encode_ciphertext_blob,
    decode_ciphertext_blob,
)

AWS_KMS_REGION = os.environ.get(
    "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
)

AES_GCM_TAG_LENGTH = 16
AES_GCM_IV_LENGTH = 12
DATA_KEY_SPEC = "AES_256"


def _generate_iv() -> bytes:
    return os.urandom(AES_GCM_IV_LENGTH)


def _aes_gcm_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> tuple[bytes, bytes]:
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend(),
    ).encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext, encryptor.tag


def _aes_gcm_decrypt(ciphertext: bytes, key: bytes, iv: bytes, tag: bytes) -> bytes:
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend(),
    ).decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext


def _build_envelope_blob(iv: bytes, tag: bytes, ciphertext: bytes) -> bytes:
    header = struct.pack("!B", 1)
    header += struct.pack("!H", len(iv))
    header += iv
    header += struct.pack("!H", len(tag))
    header += tag
    return header + ciphertext


def _parse_envelope_blob(blob: bytes) -> tuple[bytes, bytes, bytes]:
    offset = 0
    version = struct.unpack("!B", blob[offset : offset + 1])[0]
    offset += 1
    iv_len = struct.unpack("!H", blob[offset : offset + 2])[0]
    offset += 2
    iv = blob[offset : offset + iv_len]
    offset += iv_len
    tag_len = struct.unpack("!H", blob[offset : offset + 2])[0]
    offset += 2
    tag = blob[offset : offset + tag_len]
    offset += tag_len
    ciphertext = blob[offset:]
    return iv, tag, ciphertext


def envelope_encrypt(
    plaintext: Any,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    client: Optional[SecurityClient] = None,
) -> Dict[str, Any]:
    target_key_id = key_id or DEFAULT_KEY_ID
    if not target_key_id:
        raise ValueError(
            "No KMS key ID provided. Set DEFAULT_KMS_KEY_ID or pass key_id explicitly."
        )

    ctx = encryption_context or DEFAULT_ENCRYPTION_CONTEXT
    plaintext_bytes = normalize_payload_to_bytes(plaintext)

    kms_client = client or SecurityClient()

    data_key_request = GenerateDataKeyRequest(
        key_id=target_key_id,
        key_spec=DATA_KEY_SPEC,
        encryption_context=ctx,
    )
    data_key_response = kms_client.generate_data_key(data_key_request)

    plaintext_data_key = data_key_response.plaintext_key
    encrypted_data_key = data_key_response.encrypted_key
    key_id_used = data_key_response.key_id

    iv = _generate_iv()
    ciphertext, tag = _aes_gcm_encrypt(plaintext_bytes, plaintext_data_key, iv)
    envelope_blob = _build_envelope_blob(iv, tag, ciphertext)

    result = EnvelopeEncryptionResult(
        encrypted_data_key=encrypted_data_key,
        encrypted_payload=envelope_blob,
        key_id=key_id_used,
        algorithm="AES_256_GCM",
        encryption_context=ctx,
    )

    return {
        "encrypted_data_key": encode_ciphertext_blob(result.encrypted_data_key),
        "encrypted_payload": encode_ciphertext_blob(result.encrypted_payload),
        "key_id": result.key_id,
        "algorithm": result.algorithm,
        "encryption_context": result.encryption_context,
    }


def envelope_decrypt(
    encrypted_data_key: str,
    encrypted_payload: str,
    encryption_context: Optional[Dict[str, str]] = None,
    client: Optional[SecurityClient] = None,
) -> Dict[str, Any]:
    ctx = encryption_context or DEFAULT_ENCRYPTION_CONTEXT

    encrypted_data_key_bytes = decode_ciphertext_blob(encrypted_data_key)
    envelope_blob = decode_ciphertext_blob(encrypted_payload)

    kms_client = client or SecurityClient()

    decrypt_request = DecryptRequest(
        ciphertext_blob=encrypted_data_key_bytes,
        encryption_context=ctx,
    )
    decrypt_response = kms_client.decrypt(decrypt_request)

    plaintext_data_key = decrypt_response.plaintext
    key_id_used = decrypt_response.key_id

    iv, tag, ciphertext = _parse_envelope_blob(envelope_blob)
    plaintext = _aes_gcm_decrypt(ciphertext, plaintext_data_key, iv, tag)

    result = EnvelopeDecryptionResult(
        plaintext=plaintext,
        key_id=key_id_used,
    )

    return {
        "plaintext": result.plaintext.decode("utf-8", errors="replace"),
        "plaintext_bytes": result.plaintext,
        "key_id": result.key_id,
    }
