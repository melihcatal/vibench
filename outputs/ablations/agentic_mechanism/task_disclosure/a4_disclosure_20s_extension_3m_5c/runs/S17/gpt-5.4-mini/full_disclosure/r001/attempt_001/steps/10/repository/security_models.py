from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, MutableMapping, Optional
import base64


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_label_mapping(labels: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not labels:
        return {}
    normalized: Dict[str, str] = {}
    for key, value in labels.items():
        if key is None:
            continue
        normalized[str(key)] = "" if value is None else str(value)
    return normalized


def _normalize_bytes(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, memoryview):
        return value.tobytes()
    if isinstance(value, str):
        return value.encode("utf-8")
    raise TypeError(f"Unsupported binary value type: {type(value)!r}")


def _b64encode(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def _b64decode(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        value = value.decode("ascii")
    return base64.b64decode(str(value))


@dataclass(frozen=True)
class KeyIdentifier:
    key_id: str
    version: Optional[str] = None
    region: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "KeyIdentifier":
        return cls(
            key_id=str(data.get("key_id") or data.get("keyId") or data.get("name") or ""),
            version=(str(data["version"]) if data.get("version") is not None else None),
            region=(str(data["region"]) if data.get("region") is not None else None),
            labels=_normalize_label_mapping(data.get("labels") or data.get("tags")),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"key_id": self.key_id}
        if self.version is not None:
            result["version"] = self.version
        if self.region is not None:
            result["region"] = self.region
        if self.labels:
            result["labels"] = dict(self.labels)
        return result


@dataclass(frozen=True)
class EncryptRequest:
    key: KeyIdentifier
    plaintext: bytes
    aad: bytes = b""
    algorithm: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "EncryptRequest":
        return cls(
            key=KeyIdentifier.from_mapping(data.get("key") or data),
            plaintext=_normalize_bytes(data.get("plaintext")),
            aad=_normalize_bytes(data.get("aad") or data.get("associated_data")),
            algorithm=(str(data["algorithm"]) if data.get("algorithm") is not None else None),
            labels=_normalize_label_mapping(data.get("labels")),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"key": self.key.to_dict(), "plaintext_b64": _b64encode(self.plaintext)}
        if self.aad:
            result["aad_b64"] = _b64encode(self.aad)
        if self.algorithm is not None:
            result["algorithm"] = self.algorithm
        if self.labels:
            result["labels"] = dict(self.labels)
        return result


@dataclass(frozen=True)
class DecryptRequest:
    key: KeyIdentifier
    ciphertext: bytes
    aad: bytes = b""
    algorithm: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "DecryptRequest":
        return cls(
            key=KeyIdentifier.from_mapping(data.get("key") or data),
            ciphertext=_normalize_bytes(data.get("ciphertext") or data.get("ciphertext_bytes")),
            aad=_normalize_bytes(data.get("aad") or data.get("associated_data")),
            algorithm=(str(data["algorithm"]) if data.get("algorithm") is not None else None),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"key": self.key.to_dict(), "ciphertext_b64": _b64encode(self.ciphertext)}
        if self.aad:
            result["aad_b64"] = _b64encode(self.aad)
        if self.algorithm is not None:
            result["algorithm"] = self.algorithm
        return result


@dataclass(frozen=True)
class EncryptResponse:
    key: KeyIdentifier
    ciphertext: bytes
    algorithm: Optional[str] = None
    request_id: Optional[str] = None
    created_at: datetime = field(default_factory=_utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "EncryptResponse":
        return cls(
            key=KeyIdentifier.from_mapping(data.get("key") or data),
            ciphertext=_b64decode(data.get("ciphertext_b64") or data.get("ciphertext") or data.get("ciphertext_bytes")),
            algorithm=(str(data["algorithm"]) if data.get("algorithm") is not None else None),
            request_id=(str(data["request_id"]) if data.get("request_id") is not None else None),
            created_at=_parse_datetime(data.get("created_at") or data.get("timestamp")),
            metadata={k: v for k, v in dict(data).items() if k not in {"key", "ciphertext_b64", "ciphertext", "ciphertext_bytes", "algorithm", "request_id", "created_at", "timestamp"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "key": self.key.to_dict(),
            "ciphertext_b64": _b64encode(self.ciphertext),
            "created_at": self.created_at.isoformat(),
        }
        if self.algorithm is not None:
            result["algorithm"] = self.algorithm
        if self.request_id is not None:
            result["request_id"] = self.request_id
        if self.metadata:
            result.update(self.metadata)
        return result


@dataclass(frozen=True)
class DecryptResponse:
    key: KeyIdentifier
    plaintext: bytes
    algorithm: Optional[str] = None
    request_id: Optional[str] = None
    created_at: datetime = field(default_factory=_utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "DecryptResponse":
        return cls(
            key=KeyIdentifier.from_mapping(data.get("key") or data),
            plaintext=_b64decode(data.get("plaintext_b64") or data.get("plaintext") or data.get("plaintext_bytes")),
            algorithm=(str(data["algorithm"]) if data.get("algorithm") is not None else None),
            request_id=(str(data["request_id"]) if data.get("request_id") is not None else None),
            created_at=_parse_datetime(data.get("created_at") or data.get("timestamp")),
            metadata={k: v for k, v in dict(data).items() if k not in {"key", "plaintext_b64", "plaintext", "plaintext_bytes", "algorithm", "request_id", "created_at", "timestamp"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "key": self.key.to_dict(),
            "plaintext_b64": _b64encode(self.plaintext),
            "created_at": self.created_at.isoformat(),
        }
        if self.algorithm is not None:
            result["algorithm"] = self.algorithm
        if self.request_id is not None:
            result["request_id"] = self.request_id
        if self.metadata:
            result.update(self.metadata)
        return result


def _parse_datetime(value: Any) -> datetime:
    if value is None:
        return _utcnow()
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = str(value)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def normalize_encryption_request(data: Mapping[str, Any]) -> EncryptRequest:
    return EncryptRequest.from_mapping(data)


def normalize_decryption_request(data: Mapping[str, Any]) -> DecryptRequest:
    return DecryptRequest.from_mapping(data)


def normalize_encrypt_response(data: Mapping[str, Any]) -> EncryptResponse:
    return EncryptResponse.from_mapping(data)


def normalize_decrypt_response(data: Mapping[str, Any]) -> DecryptResponse:
    return DecryptResponse.from_mapping(data)
