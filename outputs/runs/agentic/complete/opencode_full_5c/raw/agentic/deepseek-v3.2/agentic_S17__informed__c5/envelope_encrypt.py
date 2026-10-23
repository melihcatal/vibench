import os
import json
from typing import Dict, Any, Optional, Tuple
import boto3
from botocore.exceptions import ClientError
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import secrets
from security_client import SecurityClient
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse


def generate_data_key(
    key_id: Optional[str] = None,
    key_spec: str = "AES_256",
    encryption_context: Optional[Dict[str, str]] = None,
) -> EnvelopeEncryptionResponse:
    client = SecurityClient()

    if not key_id:
        key_id = client.get_key_id()

    if not key_id:
        raise ValueError(
            "No key ID provided and AWS_KMS_KEY_ID environment variable not set"
        )

    if not client.validate_key_id(key_id):
        raise ValueError(f"Invalid key ID: {key_id}")

    kms_client = boto3.client("kms", region_name=client.region_name)

    try:
        response = kms_client.generate_data_key(
            KeyId=key_id, KeySpec=key_spec, EncryptionContext=encryption_context or {}
        )

        return EnvelopeEncryptionResponse(
            ciphertext_blob=response["CiphertextBlob"],
            plaintext_key=response["Plaintext"],
            key_id=response["KeyId"],
        )
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        raise RuntimeError(
            f"AWS KMS data key generation failed: {error_code} - {error_msg}"
        )


def encrypt_with_data_key(plaintext: bytes, data_key: bytes) -> Tuple[bytes, bytes]:
    iv = secrets.token_bytes(16)

    cipher = Cipher(algorithms.AES(data_key), modes.CBC(iv), backend=default_backend())

    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext, iv


def decrypt_with_data_key(ciphertext: bytes, data_key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(data_key), modes.CBC(iv), backend=default_backend())

    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext


def envelope_encrypt(
    plaintext: bytes,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    data_key_response = generate_data_key(key_id, "AES_256", encryption_context)

    ciphertext, iv = encrypt_with_data_key(plaintext, data_key_response.plaintext_key)

    client = SecurityClient()

    return {
        "encrypted_data_key": client.base64_encode(data_key_response.ciphertext_blob),
        "ciphertext": client.base64_encode(ciphertext),
        "iv": client.base64_encode(iv),
        "key_id": data_key_response.key_id,
        "encryption_context": encryption_context,
        "provider": "AWS KMS",
    }


def envelope_decrypt(
    encrypted_data_key: bytes,
    ciphertext: bytes,
    iv: bytes,
    encryption_context: Optional[Dict[str, str]] = None,
) -> bytes:
    client = SecurityClient()

    kms_client = boto3.client("kms", region_name=client.region_name)

    try:
        response = kms_client.decrypt(
            CiphertextBlob=encrypted_data_key,
            EncryptionContext=encryption_context or {},
        )

        data_key = response["Plaintext"]

        return decrypt_with_data_key(ciphertext, data_key, iv)
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        raise RuntimeError(
            f"AWS KMS envelope decryption failed: {error_code} - {error_msg}"
        )


def envelope_encrypt_from_request(
    request: EnvelopeEncryptionRequest,
) -> EnvelopeEncryptionResponse:
    return generate_data_key(
        key_id=request.key_id,
        key_spec=request.data_key_spec,
        encryption_context=request.encryption_context,
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        plaintext = sys.argv[1].encode("utf-8")
        key_id = sys.argv[2] if len(sys.argv) > 2 else None
        try:
            result = envelope_encrypt(plaintext, key_id)
            print(json.dumps(result))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
