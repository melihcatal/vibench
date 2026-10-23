import os
from typing import Optional, Dict, List

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from security_client import get_kms_client, resolve_key_id, parse_kms_error
from security_models import (
    GenerateDataKeyRequest,
    GenerateDataKeyResponse,
    EnvelopeEncryptionResult,
    EnvelopeDecryptionResult,
    validate_key_id,
    encode_ciphertext,
    normalize_plaintext,
    normalize_ciphertext,
)

AES_GCM_NONCE_SIZE = 12
AES_GCM_TAG_SIZE = 16
DATA_KEY_SPEC = "AES_256"


def generate_data_key(
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    number_of_bytes: int = 32,
    grant_tokens: Optional[List[str]] = None,
) -> GenerateDataKeyResponse:
    kms_client = get_kms_client()
    resolved_key_id = resolve_key_id(validate_key_id(key_id))

    params = {
        "KeyId": resolved_key_id,
        "KeySpec": DATA_KEY_SPEC,
    }

    if encryption_context:
        params["EncryptionContext"] = encryption_context
    if grant_tokens:
        params["GrantTokens"] = grant_tokens

    request = GenerateDataKeyRequest(
        key_id=resolved_key_id,
        key_spec=DATA_KEY_SPEC,
        number_of_bytes=number_of_bytes,
        encryption_context=encryption_context,
        grant_tokens=grant_tokens,
    )

    try:
        response = kms_client.generate_data_key(**params)
        return GenerateDataKeyResponse(
            plaintext_data_key=response["Plaintext"],
            encrypted_data_key=response["CiphertextBlob"],
            key_id=response["KeyId"],
            request_id=response["ResponseMetadata"]["RequestId"],
            http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
        )
    except Exception as e:
        error_info = parse_kms_error(e)
        raise RuntimeError(
            f"AWS KMS GenerateDataKey failed for key {resolved_key_id}: "
            f"[{error_info['error_code']}] {error_info['error_message']}"
        ) from e


def envelope_encrypt(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> EnvelopeEncryptionResult:
    data_key_response = generate_data_key(
        key_id=key_id,
        encryption_context=encryption_context,
    )
    plaintext_data_key = data_key_response.plaintext_data_key
    nonce = os.urandom(AES_GCM_NONCE_SIZE)
    plaintext_bytes = normalize_plaintext(plaintext)

    cipher = Cipher(
        algorithms.AES(plaintext_data_key),
        modes.GCM(nonce),
        backend=default_backend(),
    )
    encryptor = cipher.encryptor()
    encrypted_payload = encryptor.update(plaintext_bytes) + encryptor.finalize()
    tag = encryptor.tag

    envelope_blob = nonce + tag + encrypted_payload

    return EnvelopeEncryptionResult(
        encrypted_data_key=data_key_response.encrypted_data_key,
        encrypted_payload=envelope_blob,
        key_id=data_key_response.key_id,
        encryption_context=encryption_context,
    )


def envelope_decrypt(
    encrypted_data_key: bytes,
    encrypted_payload: bytes,
    encryption_context: Optional[Dict[str, str]] = None,
) -> EnvelopeDecryptionResult:
    kms_client = get_kms_client()

    nonce = encrypted_payload[:AES_GCM_NONCE_SIZE]
    tag = encrypted_payload[AES_GCM_NONCE_SIZE : AES_GCM_NONCE_SIZE + AES_GCM_TAG_SIZE]
    ciphertext = encrypted_payload[AES_GCM_NONCE_SIZE + AES_GCM_TAG_SIZE :]

    decrypt_params = {
        "CiphertextBlob": encrypted_data_key,
    }
    if encryption_context:
        decrypt_params["EncryptionContext"] = encryption_context

    try:
        kms_response = kms_client.decrypt(**decrypt_params)
        plaintext_data_key = kms_response["Plaintext"]
    except Exception as e:
        error_info = parse_kms_error(e)
        raise RuntimeError(
            f"AWS KMS Decrypt (envelope) failed: "
            f"[{error_info['error_code']}] {error_info['error_message']}"
        ) from e

    cipher = Cipher(
        algorithms.AES(plaintext_data_key),
        modes.GCM(nonce, tag),
        backend=default_backend(),
    )
    decryptor = cipher.decryptor()
    plaintext_bytes = decryptor.update(ciphertext) + decryptor.finalize()

    return EnvelopeDecryptionResult(
        plaintext=plaintext_bytes,
        key_id=kms_response["KeyId"],
    )


def envelope_encrypt_and_encode(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    result = envelope_encrypt(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context,
    )
    return {
        "encrypted_data_key": encode_ciphertext(result.encrypted_data_key),
        "encrypted_payload": encode_ciphertext(result.encrypted_payload),
        "key_id": result.key_id,
    }
