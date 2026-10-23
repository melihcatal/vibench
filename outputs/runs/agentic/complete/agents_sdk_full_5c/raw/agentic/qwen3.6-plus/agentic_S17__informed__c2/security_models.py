"""
security_models.py - Define local request, response, and normalization helpers
for Key Management and Encryption operations.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import base64
import json


class KeyAlgorithm(str, Enum):
    AES_256_GCM = "AES_256_GCM"
    RSA_2048 = "RSA_2048"
    RSA_4096 = "RSA_4096"
    ECC_SECG_P256K1 = "ECC_SECG_P256K1"
    HMAC_SHA_256 = "HMAC_SHA_256"


class SigningAlgorithm(str, Enum):
    RSASSA_PKCS1_V1_5_SHA_256 = "RSASSA_PKCS1_V1_5_SHA_256"
    RSASSA_PSS_SHA_256 = "RSASSA_PSS_SHA_256"
    ECDSA_SHA_256 = "ECDSA_SHA_256"
    HMAC_SHA_256 = "HMAC_SHA_256"


class EncryptionContextType(str, Enum):
    DATABASE = "database"
    STORAGE = "storage"
    MESSAGE = "message"
    API = "api"


@dataclass
class EncryptRequest:
    plaintext: bytes
    key_id: str
    encryption_algorithm: KeyAlgorithm = KeyAlgorithm.AES_256_GCM
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None


@dataclass
class EncryptResponse:
    ciphertext_blob: bytes
    key_id: str
    encryption_algorithm: str
    ciphertext_blob_b64: str = ""

    def __post_init__(self):
        if self.ciphertext_blob and not self.ciphertext_blob_b64:
            self.ciphertext_blob_b64 = base64.b64encode(self.ciphertext_blob).decode("utf-8")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ciphertext_blob_b64": self.ciphertext_blob_b64,
            "key_id": self.key_id,
            "encryption_algorithm": self.encryption_algorithm,
        }


@dataclass
class DecryptRequest:
    ciphertext_blob: bytes
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None


@dataclass
class DecryptResponse:
    plaintext: bytes
    key_id: str
    encryption_algorithm: str
    plaintext_str: str = ""

    def __post_init__(self):
        if self.plaintext and not self.plaintext_str:
            try:
                self.plaintext_str = self.plaintext.decode("utf-8")
            except UnicodeDecodeError:
                self.plaintext_str = self.plaintext.hex()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plaintext_b64": base64.b64encode(self.plaintext).decode("utf-8"),
            "key_id": self.key_id,
            "encryption_algorithm": self.encryption_algorithm,
        }


@dataclass
class EnvelopeEncryptRequest:
    plaintext: bytes
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None
    data_key_spec: str = "AES_256"


@dataclass
class EnvelopeEncryptResponse:
    encrypted_data_key: bytes
    ciphertext_blob: bytes
    key_id: str
    encrypted_data_key_b64: str = ""
    ciphertext_blob_b64: str = ""

    def __post_init__(self):
        if self.encrypted_data_key and not self.encrypted_data_key_b64:
            self.encrypted_data_key_b64 = base64.b64encode(self.encrypted_data_key).decode("utf-8")
        if self.ciphertext_blob and not self.ciphertext_blob_b64:
            self.ciphertext_blob_b64 = base64.b64encode(self.ciphertext_blob).decode("utf-8")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "encrypted_data_key_b64": self.encrypted_data_key_b64,
            "ciphertext_blob_b64": self.ciphertext_blob_b64,
            "key_id": self.key_id,
        }


@dataclass
class SignRequest:
    message: bytes
    key_id: str
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256
    message_type: str = "RAW"


@dataclass
class SignResponse:
    signature: bytes
    key_id: str
    signing_algorithm: str
    signature_b64: str = ""

    def __post_init__(self):
        if self.signature and not self.signature_b64:
            self.signature_b64 = base64.b64encode(self.signature).decode("utf-8")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signature_b64": self.signature_b64,
            "key_id": self.key_id,
            "signing_algorithm": self.signing_algorithm,
        }


@dataclass
class VerifyRequest:
    message: bytes
    signature: bytes
    key_id: str
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256
    message_type: str = "RAW"


@dataclass
class VerifyResponse:
    signature_valid: bool
    key_id: str
    signing_algorithm: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signature_valid": self.signature_valid,
            "key_id": self.key_id,
            "signing_algorithm": self.signing_algorithm,
        }


@dataclass
class KeyMetadataResponse:
    key_id: str
    key_state: str
    key_usage: str
    key_spec: str
    origin: str
    description: str = ""
    creation_date: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "key_state": self.key_state,
            "key_usage": self.key_usage,
            "key_spec": self.key_spec,
            "origin": self.origin,
            "description": self.description,
            "creation_date": self.creation_date,
        }


def normalize_encryption_context(context: Optional[Dict[str, str]], context_type: Optional[EncryptionContextType] = None) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    if context:
        normalized.update({str(k): str(v) for k, v in context.items()})
    if context_type:
        normalized["encryption_context_type"] = context_type.value
    return normalized


def decode_b64_payload(b64_string: str) -> bytes:
    return base64.b64decode(b64_string)


def encode_b64_payload(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def parse_kms_response(response_dict: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, value in response_dict.items():
        if isinstance(value, bytes):
            result[key] = base64.b64encode(value).decode("utf-8")
        elif isinstance(value, dict):
            result[key] = {str(k): str(v) for k, v in value.items()}
        else:
            result[key] = value
    return result
