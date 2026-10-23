from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, MutableMapping, Optional


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace").strip()
    return str(value).strip()


def _normalize_optional_text(value: Any) -> Optional[str]:
    text = _normalize_text(value)
    return text or None


def _normalize_mapping(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return dict(value)
    if isinstance(value, MutableMapping):
        return dict(value)
    raise TypeError("metadata must be a mapping")


def _normalize_version(value: Any) -> str:
    text = _normalize_text(value)
    return text or "latest"


@dataclass(frozen=True)
class EncryptRequest:
    plaintext: str
    key_name: str
    aad: Optional[str] = None
    algorithm: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def normalize(cls, payload: Mapping[str, Any]) -> "EncryptRequest":
        return cls(
            plaintext=_normalize_text(payload.get("plaintext")),
            key_name=_normalize_text(payload.get("key_name") or payload.get("key_id") or payload.get("key")),
            aad=_normalize_optional_text(payload.get("aad")),
            algorithm=_normalize_optional_text(payload.get("algorithm")),
            metadata=_normalize_mapping(payload.get("metadata")),
        )


@dataclass(frozen=True)
class DecryptRequest:
    ciphertext: str
    key_name: str
    aad: Optional[str] = None
    algorithm: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def normalize(cls, payload: Mapping[str, Any]) -> "DecryptRequest":
        return cls(
            ciphertext=_normalize_text(payload.get("ciphertext")),
            key_name=_normalize_text(payload.get("key_name") or payload.get("key_id") or payload.get("key")),
            aad=_normalize_optional_text(payload.get("aad")),
            algorithm=_normalize_optional_text(payload.get("algorithm")),
            metadata=_normalize_mapping(payload.get("metadata")),
        )


@dataclass(frozen=True)
class SignRequest:
    message: str
    key_name: str
    algorithm: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def normalize(cls, payload: Mapping[str, Any]) -> "SignRequest":
        return cls(
            message=_normalize_text(payload.get("message") or payload.get("payload") or payload.get("data")),
            key_name=_normalize_text(payload.get("key_name") or payload.get("key_id") or payload.get("key")),
            algorithm=_normalize_optional_text(payload.get("algorithm")),
            metadata=_normalize_mapping(payload.get("metadata")),
        )


@dataclass(frozen=True)
class VerifyRequest:
    message: str
    signature: str
    key_name: str
    algorithm: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def normalize(cls, payload: Mapping[str, Any]) -> "VerifyRequest":
        return cls(
            message=_normalize_text(payload.get("message") or payload.get("payload") or payload.get("data")),
            signature=_normalize_text(payload.get("signature")),
            key_name=_normalize_text(payload.get("key_name") or payload.get("key_id") or payload.get("key")),
            algorithm=_normalize_optional_text(payload.get("algorithm")),
            metadata=_normalize_mapping(payload.get("metadata")),
        )


@dataclass(frozen=True)
class KeyUsageRequest:
    key_name: str
    version: str = "latest"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def normalize(cls, payload: Mapping[str, Any]) -> "KeyUsageRequest":
        return cls(
            key_name=_normalize_text(payload.get("key_name") or payload.get("key_id") or payload.get("key")),
            version=_normalize_version(payload.get("version")),
            metadata=_normalize_mapping(payload.get("metadata")),
        )


@dataclass(frozen=True)
class EncryptionResponse:
    ciphertext: str
    key_name: str
    algorithm: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "EncryptionResponse":
        return cls(
            ciphertext=_normalize_text(payload.get("ciphertext") or payload.get("encrypted_text") or payload.get("result")),
            key_name=_normalize_text(payload.get("key_name") or payload.get("key_id") or payload.get("key")),
            algorithm=_normalize_optional_text(payload.get("algorithm")),
            metadata=_normalize_mapping(payload.get("metadata")),
        )


@dataclass(frozen=True)
class DecryptionResponse:
    plaintext: str
    key_name: str
    algorithm: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "DecryptionResponse":
        return cls(
            plaintext=_normalize_text(payload.get("plaintext") or payload.get("decrypted_text") or payload.get("result")),
            key_name=_normalize_text(payload.get("key_name") or payload.get("key_id") or payload.get("key")),
            algorithm=_normalize_optional_text(payload.get("algorithm")),
            metadata=_normalize_mapping(payload.get("metadata")),
        )


@dataclass(frozen=True)
class SignatureResponse:
    signature: str
    key_name: str
    algorithm: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "SignatureResponse":
        return cls(
            signature=_normalize_text(payload.get("signature") or payload.get("result")),
            key_name=_normalize_text(payload.get("key_name") or payload.get("key_id") or payload.get("key")),
            algorithm=_normalize_optional_text(payload.get("algorithm")),
            metadata=_normalize_mapping(payload.get("metadata")),
        )


@dataclass(frozen=True)
class VerificationResponse:
    verified: bool
    key_name: str
    algorithm: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "VerificationResponse":
        verified = payload.get("verified")
        if verified is None:
            verified = payload.get("valid")
        return cls(
            verified=bool(verified),
            key_name=_normalize_text(payload.get("key_name") or payload.get("key_id") or payload.get("key")),
            algorithm=_normalize_optional_text(payload.get("algorithm")),
            metadata=_normalize_mapping(payload.get("metadata")),
        )


@dataclass(frozen=True)
class KeyUsageSummary:
    key_name: str
    version: str
    encryptions: int = 0
    decryptions: int = 0
    signatures: int = 0
    verifications: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "KeyUsageSummary":
        return cls(
            key_name=_normalize_text(payload.get("key_name") or payload.get("key_id") or payload.get("key")),
            version=_normalize_version(payload.get("version")),
            encryptions=int(payload.get("encryptions", 0) or 0),
            decryptions=int(payload.get("decryptions", 0) or 0),
            signatures=int(payload.get("signatures", 0) or 0),
            verifications=int(payload.get("verifications", 0) or 0),
            metadata=_normalize_mapping(payload.get("metadata")),
        )
