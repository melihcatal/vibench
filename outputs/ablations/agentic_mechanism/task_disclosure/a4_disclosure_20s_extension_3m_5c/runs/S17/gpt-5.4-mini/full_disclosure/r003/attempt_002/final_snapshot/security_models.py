from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Union


def _coerce_bytes(value: Any) -> Optional[bytes]:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, memoryview):
        return value.tobytes()
    if isinstance(value, str):
        try:
            return value.encode("utf-8")
        except Exception:
            return None
    return None


def _coerce_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, (bytes, bytearray, memoryview)):
        try:
            return bytes(value).decode("utf-8")
        except Exception:
            return None
    return str(value)


def _normalize_metadata(value: Any) -> Dict[str, str]:
    if not isinstance(value, Mapping):
        return {}
    out: Dict[str, str] = {}
    for k, v in value.items():
        if k is None or v is None:
            continue
        out[str(k)] = _coerce_text(v) or ""
    return out


def _normalize_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Sequence):
        out: List[str] = []
        for item in value:
            text = _coerce_text(item)
            if text is not None:
                out.append(text)
        return out
    return []


def _normalize_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "y", "on"}:
            return True
        if lowered in {"false", "0", "no", "n", "off"}:
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    return None


def _normalize_int(value: Any) -> Optional[int]:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.strip())
        except Exception:
            return None
    return None


def _strip_none(data: Mapping[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


@dataclass(frozen=True)
class EncryptRequest:
    plaintext: Union[str, bytes]
    key_id: Optional[str] = None
    key_name: Optional[str] = None
    additional_authenticated_data: Optional[Union[str, bytes]] = None
    encryption_context: Optional[Mapping[str, Any]] = None
    algorithm: Optional[str] = None

    def normalized(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "plaintext": _coerce_text(self.plaintext),
                "key_id": self.key_id,
                "key_name": self.key_name,
                "additional_authenticated_data": _coerce_text(self.additional_authenticated_data),
                "encryption_context": _normalize_metadata(self.encryption_context or {}),
                "algorithm": self.algorithm,
            }
        )


@dataclass(frozen=True)
class DecryptRequest:
    ciphertext: Union[str, bytes]
    key_id: Optional[str] = None
    key_name: Optional[str] = None
    additional_authenticated_data: Optional[Union[str, bytes]] = None
    encryption_context: Optional[Mapping[str, Any]] = None
    algorithm: Optional[str] = None

    def normalized(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "ciphertext": _coerce_text(self.ciphertext),
                "key_id": self.key_id,
                "key_name": self.key_name,
                "additional_authenticated_data": _coerce_text(self.additional_authenticated_data),
                "encryption_context": _normalize_metadata(self.encryption_context or {}),
                "algorithm": self.algorithm,
            }
        )


@dataclass(frozen=True)
class SignRequest:
    message: Union[str, bytes]
    key_id: Optional[str] = None
    key_name: Optional[str] = None
    algorithm: Optional[str] = None
    prehashed: Optional[bool] = None

    def normalized(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "message": _coerce_text(self.message),
                "key_id": self.key_id,
                "key_name": self.key_name,
                "algorithm": self.algorithm,
                "prehashed": self.prehashed if self.prehashed is None else bool(self.prehashed),
            }
        )


@dataclass(frozen=True)
class VerifyRequest:
    message: Union[str, bytes]
    signature: Union[str, bytes]
    key_id: Optional[str] = None
    key_name: Optional[str] = None
    algorithm: Optional[str] = None
    prehashed: Optional[bool] = None

    def normalized(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "message": _coerce_text(self.message),
                "signature": _coerce_text(self.signature),
                "key_id": self.key_id,
                "key_name": self.key_name,
                "algorithm": self.algorithm,
                "prehashed": self.prehashed if self.prehashed is None else bool(self.prehashed),
            }
        )


@dataclass(frozen=True)
class KeyMaterial:
    key_id: Optional[str] = None
    key_name: Optional[str] = None
    version: Optional[str] = None
    algorithm: Optional[str] = None
    public_key: Optional[Union[str, bytes]] = None
    private_key: Optional[Union[str, bytes]] = None

    def normalized(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "key_id": self.key_id,
                "key_name": self.key_name,
                "version": self.version,
                "algorithm": self.algorithm,
                "public_key": _coerce_text(self.public_key),
                "private_key": _coerce_text(self.private_key),
            }
        )


@dataclass(frozen=True)
class CryptoResponse:
    success: Optional[bool] = None
    key_id: Optional[str] = None
    key_name: Optional[str] = None
    ciphertext: Optional[Union[str, bytes]] = None
    plaintext: Optional[Union[str, bytes]] = None
    signature: Optional[Union[str, bytes]] = None
    verified: Optional[bool] = None
    algorithm: Optional[str] = None
    version: Optional[str] = None
    metadata: Optional[Mapping[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "CryptoResponse":
        return cls(
            success=_normalize_bool(data.get("success")),
            key_id=_coerce_text(data.get("key_id")),
            key_name=_coerce_text(data.get("key_name")),
            ciphertext=data.get("ciphertext"),
            plaintext=data.get("plaintext"),
            signature=data.get("signature"),
            verified=_normalize_bool(data.get("verified")),
            algorithm=_coerce_text(data.get("algorithm")),
            version=_coerce_text(data.get("version")),
            metadata=data.get("metadata") if isinstance(data.get("metadata"), Mapping) else None,
        )

    def normalized(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "success": self.success,
                "key_id": self.key_id,
                "key_name": self.key_name,
                "ciphertext": _coerce_text(self.ciphertext),
                "plaintext": _coerce_text(self.plaintext),
                "signature": _coerce_text(self.signature),
                "verified": self.verified,
                "algorithm": self.algorithm,
                "version": self.version,
                "metadata": dict(self.metadata) if isinstance(self.metadata, Mapping) else None,
            }
        )


def normalize_request(value: Any) -> Dict[str, Any]:
    if hasattr(value, "normalized") and callable(getattr(value, "normalized")):
        normalized = value.normalized()
        if isinstance(normalized, Mapping):
            return dict(normalized)
    if isinstance(value, Mapping):
        return dict(value)
    if isinstance(value, (str, bytes, bytearray, memoryview)):
        return {"value": _coerce_text(value)}
    return {"value": value}


def normalize_response(value: Any) -> Dict[str, Any]:
    if isinstance(value, CryptoResponse):
        return value.normalized()
    if hasattr(value, "normalized") and callable(getattr(value, "normalized")):
        normalized = value.normalized()
        if isinstance(normalized, Mapping):
            return dict(normalized)
    if isinstance(value, Mapping):
        return {
            "success": _normalize_bool(value.get("success")),
            "key_id": _coerce_text(value.get("key_id")),
            "key_name": _coerce_text(value.get("key_name")),
            "ciphertext": _coerce_text(value.get("ciphertext")),
            "plaintext": _coerce_text(value.get("plaintext")),
            "signature": _coerce_text(value.get("signature")),
            "verified": _normalize_bool(value.get("verified")),
            "algorithm": _coerce_text(value.get("algorithm")),
            "version": _coerce_text(value.get("version")),
            "metadata": dict(value.get("metadata")) if isinstance(value.get("metadata"), Mapping) else None,
        }
    return {"value": value}


def normalize_key_usage_events(events: Any) -> List[Dict[str, Any]]:
    if events is None:
        return []
    if isinstance(events, Mapping):
        events = [events]
    if not isinstance(events, Iterable) or isinstance(events, (str, bytes, bytearray, memoryview)):
        return []
    normalized: List[Dict[str, Any]] = []
    for event in events:
        if isinstance(event, Mapping):
            normalized.append(
                _strip_none(
                    {
                        "event_type": _coerce_text(event.get("event_type") or event.get("type")),
                        "key_id": _coerce_text(event.get("key_id")),
                        "key_name": _coerce_text(event.get("key_name")),
                        "algorithm": _coerce_text(event.get("algorithm")),
                        "timestamp": _coerce_text(event.get("timestamp") or event.get("time")),
                        "count": _normalize_int(event.get("count")),
                        "status": _coerce_text(event.get("status")),
                        "metadata": dict(event.get("metadata")) if isinstance(event.get("metadata"), Mapping) else None,
                    }
                )
            )
    return normalized


def normalize_encryption_context(context: Any) -> Dict[str, str]:
    return _normalize_metadata(context)


def normalize_signing_algorithm(algorithm: Any) -> Optional[str]:
    return _coerce_text(algorithm)


def normalize_key_identifier(value: Any) -> Optional[str]:
    return _coerce_text(value)


def normalize_plaintext(value: Any) -> Optional[str]:
    return _coerce_text(value)


def normalize_ciphertext(value: Any) -> Optional[str]:
    return _coerce_text(value)
