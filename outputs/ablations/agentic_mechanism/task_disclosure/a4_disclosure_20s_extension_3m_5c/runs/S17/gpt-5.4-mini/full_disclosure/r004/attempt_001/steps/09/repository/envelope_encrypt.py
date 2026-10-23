import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

try:
    from aws_encryption_sdk import CommitmentPolicy, EncryptionSDKClient
    from aws_encryption_sdk.keyrings.aws_kms import AwsKmsKeyring
except Exception:
    EncryptionSDKClient = None
    CommitmentPolicy = None
    AwsKmsKeyring = None


@dataclass
class EnvelopeEncryptionResult:
    ciphertext: str
    encrypted_data_key: str
    key_id: str
    provider: str = "aws-kms"


def _build_keyring(kms_key_id: str):
    if AwsKmsKeyring is None:
        raise RuntimeError("aws-encryption-sdk is required for AWS KMS envelope encryption")
    return AwsKmsKeyring(generator_key_id=kms_key_id)


def envelope_encrypt(plaintext: str, kms_key_id: Optional[str] = None, aad: Optional[Dict[str, Any]] = None) -> EnvelopeEncryptionResult:
    kms_key_id = kms_key_id or os.environ.get("AWS_KMS_KEY_ID")
    if not kms_key_id:
        raise ValueError("kms_key_id or AWS_KMS_KEY_ID is required")

    if EncryptionSDKClient is not None and AwsKmsKeyring is not None:
        client = EncryptionSDKClient(commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT)
        keyring = _build_keyring(kms_key_id)
        encryption_context = {k: str(v) for k, v in (aad or {}).items()}
        ciphertext, header = client.encrypt(source=plaintext.encode("utf-8"), keyring=keyring, encryption_context=encryption_context)
        encrypted_data_key = base64.b64encode(header.encrypted_data_keys[0].encrypted_data_key).decode("utf-8") if header.encrypted_data_keys else ""
        return EnvelopeEncryptionResult(
            ciphertext=base64.b64encode(ciphertext).decode("utf-8"),
            encrypted_data_key=encrypted_data_key,
            key_id=kms_key_id,
        )

    raise RuntimeError("AWS Encryption SDK is not installed")


def _aesgcm_encrypt(key: bytes, plaintext: bytes, aad: Optional[bytes] = None) -> Dict[str, str]:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext, aad)
    return {
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.b64encode(ct).decode("utf-8"),
    }


def encrypt_payload_with_data_key(data_key_b64: str, plaintext: str, aad: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    data_key = base64.b64decode(data_key_b64)
    aad_bytes = json.dumps(aad or {}, sort_keys=True).encode("utf-8") if aad else None
    return _aesgcm_encrypt(data_key, plaintext.encode("utf-8"), aad_bytes)
