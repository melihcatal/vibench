from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class KeyStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING_DELETION = "pending_deletion"


class EncryptionAlgorithm(str, Enum):
    AES_256_GCM = "AES-256-GCM"
    RSA_OAEP_SHA256 = "RSA-OAEP-SHA256"
    CHACHA20_POLY1305 = "CHACHA20-POLY1305"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _to_utc_iso(value: Optional[datetime] = None) -> str:
    value = value or _utc_now()
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value).strip()


def _normalize_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y", "on"}:
        return True
    if text in {"false", "0", "no", "n", "off"}:
        return False
    return default


def _normalize_enum(value: Any, enum_cls: type[Enum], default: Enum) -> Enum:
    if isinstance(value, enum_cls):
        return value
    if value is None:
        return default
    text = str(value).strip()
    for member in enum_cls:
        if text == member.value or text.lower() == member.name.lower():
            return member
    return default


def _normalize_datetime(value: Any, default: Optional[datetime] = None) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if value is None:
        return default or _utc_now()
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return default or _utc_now()
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


@dataclass(frozen=True)
class KeyCreateRequest:
    name: str
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.AES_256_GCM
    key_length: int = 256
    tags: Dict[str, str] = field(default_factory=dict)

    def normalized(self) -> "KeyCreateRequest":
        return KeyCreateRequest(
            name=_normalize_str(self.name),
            algorithm=_normalize_enum(self.algorithm, EncryptionAlgorithm, EncryptionAlgorithm.AES_256_GCM),
            key_length=int(self.key_length) if self.key_length else 256,
            tags={_normalize_str(k): _normalize_str(v) for k, v in (self.tags or {}).items() if _normalize_str(k)},
        )

    def to_dict(self) -> Dict[str, Any]:
        n = self.normalized()
        return {
            "name": n.name,
            "algorithm": n.algorithm.value,
            "key_length": n.key_length,
            "tags": n.tags,
        }


@dataclass(frozen=True)
class KeyResponse:
    key_id: str
    name: str
    algorithm: EncryptionAlgorithm
    key_length: int
    status: KeyStatus
    created_at: datetime
    updated_at: datetime
    tags: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KeyResponse":
        return cls(
            key_id=_normalize_str(data.get("key_id") or data.get("id")),
            name=_normalize_str(data.get("name")),
            algorithm=_normalize_enum(data.get("algorithm"), EncryptionAlgorithm, EncryptionAlgorithm.AES_256_GCM),
            key_length=int(data.get("key_length") or 256),
            status=_normalize_enum(data.get("status"), KeyStatus, KeyStatus.ACTIVE),
            created_at=_normalize_datetime(data.get("created_at")),
            updated_at=_normalize_datetime(data.get("updated_at"), default=_normalize_datetime(data.get("created_at"))),
            tags={_normalize_str(k): _normalize_str(v) for k, v in (data.get("tags") or {}).items() if _normalize_str(k)},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "name": self.name,
            "algorithm": self.algorithm.value,
            "key_length": self.key_length,
            "status": self.status.value,
            "created_at": _to_utc_iso(self.created_at),
            "updated_at": _to_utc_iso(self.updated_at),
            "tags": self.tags,
        }


@dataclass(frozen=True)
class EncryptRequest:
    key_id: str
    plaintext: str
    associated_data: str = ""

    def normalized(self) -> "EncryptRequest":
        return EncryptRequest(
            key_id=_normalize_str(self.key_id),
            plaintext=_normalize_str(self.plaintext),
            associated_data=_normalize_str(self.associated_data),
        )

    def to_dict(self) -> Dict[str, Any]:
        n = self.normalized()
        return {
            "key_id": n.key_id,
            "plaintext": n.plaintext,
            "associated_data": n.associated_data,
        }


@dataclass(frozen=True)
class EncryptResponse:
    key_id: str
    ciphertext: str
    algorithm: EncryptionAlgorithm
    nonce: str
    associated_data: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EncryptResponse":
        return cls(
            key_id=_normalize_str(data.get("key_id")),
            ciphertext=_normalize_str(data.get("ciphertext")),
            algorithm=_normalize_enum(data.get("algorithm"), EncryptionAlgorithm, EncryptionAlgorithm.AES_256_GCM),
            nonce=_normalize_str(data.get("nonce")),
            associated_data=_normalize_str(data.get("associated_data")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "ciphertext": self.ciphertext,
            "algorithm": self.algorithm.value,
            "nonce": self.nonce,
            "associated_data": self.associated_data,
        }


@dataclass(frozen=True)
class DecryptRequest:
    key_id: str
    ciphertext: str
    nonce: str
    associated_data: str = ""

    def normalized(self) -> "DecryptRequest":
        return DecryptRequest(
            key_id=_normalize_str(self.key_id),
            ciphertext=_normalize_str(self.ciphertext),
            nonce=_normalize_str(self.nonce),
            associated_data=_normalize_str(self.associated_data),
        )

    def to_dict(self) -> Dict[str, Any]:
        n = self.normalized()
        return {
            "key_id": n.key_id,
            "ciphertext": n.ciphertext,
            "nonce": n.nonce,
            "associated_data": n.associated_data,
        }


@dataclass(frozen=True)
class DecryptResponse:
    key_id: str
    plaintext: str
    algorithm: EncryptionAlgorithm
    verified: bool = True

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DecryptResponse":
        return cls(
            key_id=_normalize_str(data.get("key_id")),
            plaintext=_normalize_str(data.get("plaintext")),
            algorithm=_normalize_enum(data.get("algorithm"), EncryptionAlgorithm, EncryptionAlgorithm.AES_256_GCM),
            verified=_normalize_bool(data.get("verified"), default=True),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "plaintext": self.plaintext,
            "algorithm": self.algorithm.value,
            "verified": self.verified,
        }
