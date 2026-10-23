from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


def _normalize_value(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, Mapping):
        return {str(k): _normalize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize_value(v) for v in value]
    if isinstance(value, tuple):
        return tuple(_normalize_value(v) for v in value)
    return value


def normalize_metadata(metadata: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    if not metadata:
        return {}
    return {str(key).strip(): _normalize_value(value) for key, value in metadata.items() if str(key).strip()}


def normalize_key_name(name: str) -> str:
    normalized = str(name).strip()
    if not normalized:
        raise ValueError("key name must not be empty")
    return normalized


def normalize_plaintext(plaintext: str) -> str:
    normalized = str(plaintext)
    if not normalized:
        raise ValueError("plaintext must not be empty")
    return normalized


def normalize_ciphertext(ciphertext: str) -> str:
    normalized = str(ciphertext).strip()
    if not normalized:
        raise ValueError("ciphertext must not be empty")
    return normalized


@dataclass(frozen=True)
class KeyReference:
    key_name: str
    key_version: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "key_name", normalize_key_name(self.key_name))
        object.__setattr__(self, "key_version", self.key_version.strip() if isinstance(self.key_version, str) and self.key_version.strip() else None)
        object.__setattr__(self, "metadata", normalize_metadata(self.metadata))


@dataclass(frozen=True)
class EncryptRequest:
    key: KeyReference
    plaintext: str
    associated_data: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "plaintext", normalize_plaintext(self.plaintext))
        if self.associated_data is not None:
            object.__setattr__(self, "associated_data", str(self.associated_data))
        object.__setattr__(self, "metadata", normalize_metadata(self.metadata))


@dataclass(frozen=True)
class DecryptRequest:
    key: KeyReference
    ciphertext: str
    associated_data: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "ciphertext", normalize_ciphertext(self.ciphertext))
        if self.associated_data is not None:
            object.__setattr__(self, "associated_data", str(self.associated_data))
        object.__setattr__(self, "metadata", normalize_metadata(self.metadata))


@dataclass(frozen=True)
class SignRequest:
    key: KeyReference
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "message", normalize_plaintext(self.message))
        object.__setattr__(self, "metadata", normalize_metadata(self.metadata))


@dataclass(frozen=True)
class VerifyRequest:
    key: KeyReference
    message: str
    signature: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "message", normalize_plaintext(self.message))
        object.__setattr__(self, "signature", normalize_ciphertext(self.signature))
        object.__setattr__(self, "metadata", normalize_metadata(self.metadata))


@dataclass(frozen=True)
class CryptoResponse:
    key: KeyReference
    algorithm: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.algorithm is not None:
            object.__setattr__(self, "algorithm", self.algorithm.strip() or None)
        object.__setattr__(self, "metadata", normalize_metadata(self.metadata))


@dataclass(frozen=True)
class EncryptResponse(CryptoResponse):
    ciphertext: str = ""
    key_version: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()
        object.__setattr__(self, "ciphertext", normalize_ciphertext(self.ciphertext))
        if self.key_version is not None:
            object.__setattr__(self, "key_version", self.key_version.strip() or None)


@dataclass(frozen=True)
class DecryptResponse(CryptoResponse):
    plaintext: str = ""

    def __post_init__(self) -> None:
        super().__post_init__()
        object.__setattr__(self, "plaintext", normalize_plaintext(self.plaintext))


@dataclass(frozen=True)
class SignResponse(CryptoResponse):
    signature: str = ""

    def __post_init__(self) -> None:
        super().__post_init__()
        object.__setattr__(self, "signature", normalize_ciphertext(self.signature))


@dataclass(frozen=True)
class VerifyResponse(CryptoResponse):
    valid: bool = False


@dataclass(frozen=True)
class NormalizedPayload:
    data: Dict[str, Any]

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "NormalizedPayload":
        return cls(data=normalize_metadata(payload))
