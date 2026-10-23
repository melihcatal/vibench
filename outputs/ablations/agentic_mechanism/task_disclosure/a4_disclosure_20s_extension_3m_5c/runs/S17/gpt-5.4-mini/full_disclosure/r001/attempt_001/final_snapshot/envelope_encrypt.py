import base64
import json
import os
from typing import Optional

import boto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def _b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def _b64decode(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


def envelope_encrypt(plaintext: str, kms_key_id: Optional[str] = None, context: Optional[dict] = None) -> str:
    key_id = kms_key_id or os.environ.get("AWS_KMS_KEY_ID") or os.environ.get("AWS_KMS_KEY_ARN")
    if not key_id:
        raise ValueError("AWS KMS key id/arn is required")

    kms = boto3.client("kms")
    generate_kwargs = {"KeyId": key_id, "KeySpec": "AES_256"}
    if context:
        generate_kwargs["EncryptionContext"] = {str(k): str(v) for k, v in context.items()}
    response = kms.generate_data_key(**generate_kwargs)

    plaintext_key = response["Plaintext"]
    encrypted_key = response["CiphertextBlob"]
    nonce = os.urandom(12)
    aesgcm = AESGCM(plaintext_key)
    aad = json.dumps(context or {}, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), aad)

    payload = {
        "provider": "aws-kms",
        "key_id": key_id,
        "encrypted_data_key": _b64encode(encrypted_key),
        "nonce": _b64encode(nonce),
        "ciphertext": _b64encode(ciphertext),
        "aad": _b64encode(aad),
    }
    return json.dumps(payload, separators=(",", ":"))


def envelope_decrypt(payload_json: str, context: Optional[dict] = None) -> str:
    payload = json.loads(payload_json)
    if payload.get("provider") != "aws-kms":
        raise ValueError("Unsupported provider")

    kms = boto3.client("kms")
    encrypted_key = _b64decode(payload["encrypted_data_key"])
    nonce = _b64decode(payload["nonce"])
    ciphertext = _b64decode(payload["ciphertext"])
    aad = _b64decode(payload.get("aad", "")) if payload.get("aad") else json.dumps(context or {}, sort_keys=True, separators=(",", ":")).encode("utf-8")

    decrypt_kwargs = {"CiphertextBlob": encrypted_key}
    if context:
        decrypt_kwargs["EncryptionContext"] = {str(k): str(v) for k, v in context.items()}
    data_key = kms.decrypt(**decrypt_kwargs)["Plaintext"]
    plaintext = AESGCM(data_key).decrypt(nonce, ciphertext, aad)
    return plaintext.decode("utf-8")
