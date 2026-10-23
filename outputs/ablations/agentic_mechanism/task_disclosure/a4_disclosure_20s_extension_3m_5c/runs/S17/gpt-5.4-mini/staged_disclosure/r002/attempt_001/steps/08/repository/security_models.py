from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional
import base64
import hashlib
import json


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return str(value).strip() or None


def _normalize_mapping(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return dict(value)
    raise TypeError("Expected a mapping")


def _normalize_bytes(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    if isinstance(value, bytearray):
        return bytes(value)
    raise TypeError("Expected bytes-like content")


def _b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _b64decode(data: str) -> bytes:
    return base64.b64decode(data.encode("ascii"))


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_dumps(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True)
class KeyCreationRequest:
    key_name: str
    algorithm: str = "AES-256-GCM"
    purpose: str = "encryption"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "KeyCreationRequest":
        return cls(
            key_name=_normalize_str(payload.get("key_name")) or "",
            algorithm=_normalize_str(payload.get("algorithm")) or "AES-256-GCM",
            purpose=_normalize_str(payload.get("purpose")) or "encryption",
            metadata=_normalize_mapping(payload.get("metadata")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_name": self.key_name,
            "algorithm": self.algorithm,
            "purpose": self.purpose,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class KeyCreationResponse:
    key_id: str
    key_name: str
    algorithm: str
    created_at: datetime
    status: str = "active"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "KeyCreationResponse":
        created_at_raw = payload.get("created_at")
        created_at = (
            datetime.fromisoformat(created_at_raw.replace("Z", "+00:00"))
            if isinstance(created_at_raw, str)
            else _utc_now()
        )
        return cls(
            key_id=_normalize_str(payload.get("key_id")) or "",
            key_name=_normalize_str(payload.get("key_name")) or "",
            algorithm=_normalize_str(payload.get("algorithm")) or "AES-256-GCM",
            created_at=created_at,
            status=_normalize_str(payload.get("status")) or "active",
            metadata=_normalize_mapping(payload.get("metadata")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "key_name": self.key_name,
            "algorithm": self.algorithm,
            "created_at": self.created_at.astimezone(timezone.utc).isoformat(),
            "status": self.status,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class EncryptionRequest:
    plaintext: bytes
    key_id: str
    nonce: Optional[bytes] = None
    associated_data: Optional[bytes] = None

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "EncryptionRequest":
        nonce = payload.get("nonce")
        aad = payload.get("associated_data")
        return cls(
            plaintext=_normalize_bytes(payload.get("plaintext")),
            key_id=_normalize_str(payload.get("key_id")) or "",
            nonce=_normalize_bytes(nonce) if nonce is not None else None,
            associated_data=_normalize_bytes(aad) if aad is not None else None,
        )

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "plaintext": _b64encode(self.plaintext),
            "key_id": self.key_id,
        }
        if self.nonce is not None:
            data["nonce"] = _b64encode(self.nonce)
        if self.associated_data is not None:
            data["associated_data"] = _b64encode(self.associated_data)
        return data


@dataclass(frozen=True)
class EncryptionResponse:
    ciphertext: bytes
    key_id: str
    nonce: Optional[bytes] = None
    tag: Optional[bytes] = None
    algorithm: str = "AES-256-GCM"

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "EncryptionResponse":
        nonce = payload.get("nonce")
        tag = payload.get("tag")
        return cls(
            ciphertext=_normalize_bytes(_b64decode(_normalize_str(payload.get("ciphertext")) or "")),
            key_id=_normalize_str(payload.get("key_id")) or "",
            nonce=_normalize_bytes(_b64decode(_normalize_str(nonce) or "")) if nonce is not None else None,
            tag=_normalize_bytes(_b64decode(_normalize_str(tag) or "")) if tag is not None else None,
            algorithm=_normalize_str(payload.get("algorithm")) or "AES-256-GCM",
        )

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "ciphertext": _b64encode(self.ciphertext),
            "key_id": self.key_id,
            "algorithm": self.algorithm,
        }
        if self.nonce is not None:
            data["nonce"] = _b64encode(self.nonce)
        if self.tag is not None:
            data["tag"] = _b64encode(self.tag)
        return data


@dataclass(frozen=True)
class NormalizedKeyRecord:
    key_id: str
    key_name: str
    algorithm: str
    status: str
    fingerprint: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "NormalizedKeyRecord":
        normalized = _normalize_mapping(payload.get("metadata"))
        basis = _json_dumps({
            "key_id": _normalize_str(payload.get("key_id")) or "",
            "key_name": _normalize_str(payload.get("key_name")) or "",
            "algorithm": _normalize_str(payload.get("algorithm")) or "",
            "status": _normalize_str(payload.get("status")) or "",
            "metadata": normalized,
        }).encode("utf-8")
        return cls(
            key_id=_normalize_str(payload.get("key_id")) or "",
            key_name=_normalize_str(payload.get("key_name")) or "",
            algorithm=_normalize_str(payload.get("algorithm")) or "AES-256-GCM",
            status=_normalize_str(payload.get("status")) or "active",
            fingerprint=_sha256_hex(basis),
            metadata=normalized,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "key_name": self.key_name,
            "algorithm": self.algorithm,
            "status": self.status,
            "fingerprint": self.fingerprint,
            "metadata": self.metadata,
        }


def normalize_key_creation_request(payload: Mapping[str, Any]) -> Dict[str, Any]:
    return KeyCreationRequest.from_dict(payload).to_dict()


def normalize_key_creation_response(payload: Mapping[str, Any]) -> Dict[str, Any]:
    return KeyCreationResponse.from_dict(payload).to_dict()


def normalize_encryption_request(payload: Mapping[str, Any]) -> Dict[str, Any]:
    return EncryptionRequest.from_dict(payload).to_dict()


def normalize_encryption_response(payload: Mapping[str, Any]) -> Dict[str, Any]:
    return EncryptionResponse.from_dict(payload).to_dict()


def normalize_key_record(payload: Mapping[str, Any]) -> Dict[str, Any]:
    return NormalizedKeyRecord.from_dict(payload).to_dict()
