"""
Local helper: Define request, response, and normalization helpers for Key Management and Encryption.
Provider-agnostic models used across the encryption workflow.
"""

from __future__ import annotations

import base64
import dataclasses
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class EncryptionAlgorithm(str, Enum):
    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    RSAES_OAEP_SHA_1 = "RSAES_OAEP_SHA_1"
    RSAES_OAEP_SHA_256 = "RSAES_OAEP_SHA_256"


class SigningAlgorithm(str, Enum):
    RSASSA_PKCS1_V1_5_SHA_256 = "RSASSA_PKCS1_V1_5_SHA_256"
    RSASSA_PSS_SHA_256 = "RSASSA_PSS_SHA_256"
    ECDSA_SHA_256 = "ECDSA_SHA_256"


@dataclasses.dataclass
class EncryptRequest:
    key_id: str
    plaintext: bytes
    encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT
    encryption_context: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "key_id": self.key_id,
            "plaintext": self.plaintext,
        }
        if self.encryption_algorithm:
            result["encryption_algorithm"] = self.encryption_algorithm.value
        if self.encryption_context:
            result["encryption_context"] = self.encryption_context
        return result


@dataclasses.dataclass
class EncryptResponse:
    ciphertext_blob: bytes
    key_id: str
    encryption_algorithm: str
    request_id: Optional[str] = None
    timestamp: Optional[datetime] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "EncryptResponse":
        return EncryptResponse(
            ciphertext_blob=data.get("ciphertext_blob", b""),
            key_id=data.get("key_id", ""),
            encryption_algorithm=data.get("encryption_algorithm", ""),
            request_id=data.get("request_id"),
            timestamp=data.get("timestamp"),
        )


@dataclasses.dataclass
class DecryptRequest:
    key_id: Optional[str]
    ciphertext_blob: bytes
    encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT
    encryption_context: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "ciphertext_blob": self.ciphertext_blob,
        }
        if self.key_id:
            result["key_id"] = self.key_id
        if self.encryption_algorithm:
            result["encryption_algorithm"] = self.encryption_algorithm.value
        if self.encryption_context:
            result["encryption_context"] = self.encryption_context
        return result


@dataclasses.dataclass
class DecryptResponse:
    plaintext: bytes
    key_id: str
    encryption_algorithm: str
    request_id: Optional[str] = None
    timestamp: Optional[datetime] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "DecryptResponse":
        return DecryptResponse(
            plaintext=data.get("plaintext", b""),
            key_id=data.get("key_id", ""),
            encryption_algorithm=data.get("encryption_algorithm", ""),
            request_id=data.get("request_id"),
            timestamp=data.get("timestamp"),
        )


@dataclasses.dataclass
class EnvelopeEncryptResponse:
    encrypted_data_key: bytes
    plaintext_data_key: bytes
    ciphertext: bytes
    key_id: str
    iv: bytes
    algorithm: str
    request_id: Optional[str] = None


@dataclasses.dataclass
class SignRequest:
    key_id: str
    message: bytes
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PKCS1_V1_5_SHA_256
    message_type: str = "RAW"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "message": self.message,
            "signing_algorithm": self.signing_algorithm.value,
            "message_type": self.message_type,
        }


@dataclasses.dataclass
class SignResponse:
    signature: bytes
    key_id: str
    signing_algorithm: str
    request_id: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SignResponse":
        return SignResponse(
            signature=data.get("signature", b""),
            key_id=data.get("key_id", ""),
            signing_algorithm=data.get("signing_algorithm", ""),
            request_id=data.get("request_id"),
        )


@dataclasses.dataclass
class VerifyRequest:
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PKCS1_V1_5_SHA_256
    message_type: str = "RAW"


@dataclasses.dataclass
class VerifyResponse:
    signature_valid: bool
    key_id: str
    request_id: Optional[str] = None


def encode_bytes_to_base64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def decode_base64_to_bytes(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


def normalize_key_id(key_identifier: str) -> str:
    if key_identifier.startswith("arn:"):
        return key_identifier
    if key_identifier.startswith("alias/"):
        return key_identifier
    return key_identifier


def build_encryption_context(
    tenant_id: Optional[str] = None,
    resource_id: Optional[str] = None,
    extra: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    context: Dict[str, str] = {}
    if tenant_id:
        context["tenant_id"] = tenant_id
    if resource_id:
        context["resource_id"] = resource_id
    if extra:
        context.update(extra)
    return context
