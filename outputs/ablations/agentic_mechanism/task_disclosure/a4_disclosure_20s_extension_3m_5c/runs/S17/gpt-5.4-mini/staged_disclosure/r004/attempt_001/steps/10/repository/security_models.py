from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _normalize_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    return default


def _normalize_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _normalize_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


@dataclass(frozen=True)
class KeyManagementRequest:
    key_id: Optional[str] = None
    key_name: Optional[str] = None
    algorithm: Optional[str] = None
    key_size: Optional[int] = None
    purpose: Optional[str] = None
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "KeyManagementRequest":
        return cls(
            key_id=_normalize_str(data.get("key_id")),
            key_name=_normalize_str(data.get("key_name")),
            algorithm=_normalize_str(data.get("algorithm")),
            key_size=_normalize_int(data.get("key_size")),
            purpose=_normalize_str(data.get("purpose")),
            enabled=_normalize_bool(data.get("enabled"), default=True),
            metadata=_normalize_mapping(data.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "key_id": self.key_id,
            "key_name": self.key_name,
            "algorithm": self.algorithm,
            "key_size": self.key_size,
            "purpose": self.purpose,
            "enabled": self.enabled,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class EncryptionRequest:
    key_id: Optional[str] = None
    plaintext: Optional[str] = None
    plaintext_b64: Optional[str] = None
    encryption_context: dict[str, Any] = field(default_factory=dict)
    algorithm: Optional[str] = None
    associated_data: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EncryptionRequest":
        return cls(
            key_id=_normalize_str(data.get("key_id")),
            plaintext=_normalize_str(data.get("plaintext")),
            plaintext_b64=_normalize_str(data.get("plaintext_b64")),
            encryption_context=_normalize_mapping(data.get("encryption_context")),
            algorithm=_normalize_str(data.get("algorithm")),
            associated_data=_normalize_str(data.get("associated_data")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "key_id": self.key_id,
            "plaintext": self.plaintext,
            "plaintext_b64": self.plaintext_b64,
            "encryption_context": dict(self.encryption_context),
            "algorithm": self.algorithm,
            "associated_data": self.associated_data,
        }


@dataclass(frozen=True)
class KeyManagementResponse:
    key_id: str
    key_name: Optional[str] = None
    algorithm: Optional[str] = None
    key_size: Optional[int] = None
    status: Optional[str] = None
    created_at: str = field(default_factory=_utc_now_iso)
    updated_at: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "KeyManagementResponse":
        return cls(
            key_id=_normalize_str(data.get("key_id")) or "",
            key_name=_normalize_str(data.get("key_name")),
            algorithm=_normalize_str(data.get("algorithm")),
            key_size=_normalize_int(data.get("key_size")),
            status=_normalize_str(data.get("status")),
            created_at=_normalize_str(data.get("created_at")) or _utc_now_iso(),
            updated_at=_normalize_str(data.get("updated_at")),
            metadata=_normalize_mapping(data.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "key_id": self.key_id,
            "key_name": self.key_name,
            "algorithm": self.algorithm,
            "key_size": self.key_size,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class EncryptionResponse:
    key_id: str
    ciphertext: Optional[str] = None
    ciphertext_b64: Optional[str] = None
    iv: Optional[str] = None
    tag: Optional[str] = None
    algorithm: Optional[str] = None
    encrypted_at: str = field(default_factory=_utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EncryptionResponse":
        return cls(
            key_id=_normalize_str(data.get("key_id")) or "",
            ciphertext=_normalize_str(data.get("ciphertext")),
            ciphertext_b64=_normalize_str(data.get("ciphertext_b64")),
            iv=_normalize_str(data.get("iv")),
            tag=_normalize_str(data.get("tag")),
            algorithm=_normalize_str(data.get("algorithm")),
            encrypted_at=_normalize_str(data.get("encrypted_at")) or _utc_now_iso(),
            metadata=_normalize_mapping(data.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "key_id": self.key_id,
            "ciphertext": self.ciphertext,
            "ciphertext_b64": self.ciphertext_b64,
            "iv": self.iv,
            "tag": self.tag,
            "algorithm": self.algorithm,
            "encrypted_at": self.encrypted_at,
            "metadata": dict(self.metadata),
        }


def normalize_key_management_request(data: Mapping[str, Any]) -> KeyManagementRequest:
    return KeyManagementRequest.from_dict(data)


def normalize_encryption_request(data: Mapping[str, Any]) -> EncryptionRequest:
    return EncryptionRequest.from_dict(data)


def normalize_key_management_response(data: Mapping[str, Any]) -> KeyManagementResponse:
    return KeyManagementResponse.from_dict(data)


def normalize_encryption_response(data: Mapping[str, Any]) -> EncryptionResponse:
    return EncryptionResponse.from_dict(data)
