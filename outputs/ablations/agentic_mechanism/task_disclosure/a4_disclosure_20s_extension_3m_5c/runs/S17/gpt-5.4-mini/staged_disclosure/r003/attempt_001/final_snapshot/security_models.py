import base64
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Union


def _b64encode(data: Union[str, bytes]) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return base64.b64encode(data).decode("ascii")


def _b64decode(data: Union[str, bytes]) -> bytes:
    if isinstance(data, bytes):
        data = data.decode("ascii")
    return base64.b64decode(data)


def _normalize_text(value: Optional[Union[str, bytes]]) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value


def _normalize_bytes(value: Optional[Union[str, bytes]]) -> Optional[bytes]:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value
    return value.encode("utf-8")


def _normalize_ciphertext(value: Optional[Union[str, bytes]]) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, bytes):
        return _b64encode(value)
    try:
        decoded = _b64decode(value)
        return _b64encode(decoded)
    except Exception:
        return _b64encode(value)


@dataclass(frozen=True)
class KeyManagementRequest:
    key_name: str
    plaintext: Optional[Union[str, bytes]] = None
    ciphertext: Optional[Union[str, bytes]] = None
    message: Optional[Union[str, bytes]] = None
    signature: Optional[Union[str, bytes]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "KeyManagementRequest":
        return KeyManagementRequest(
            key_name=self.key_name,
            plaintext=_normalize_text(self.plaintext),
            ciphertext=_normalize_ciphertext(self.ciphertext),
            message=_normalize_text(self.message),
            signature=_normalize_ciphertext(self.signature),
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class KeyManagementResponse:
    key_name: str
    ciphertext: Optional[str] = None
    plaintext: Optional[bytes] = None
    signature: Optional[str] = None
    verified: Optional[bool] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "KeyManagementResponse":
        return cls(
            key_name=str(data["key_name"]),
            ciphertext=_normalize_ciphertext(data.get("ciphertext")),
            plaintext=_normalize_bytes(data.get("plaintext")),
            signature=_normalize_ciphertext(data.get("signature")),
            verified=data.get("verified"),
            metadata=dict(data.get("metadata", {})),
        )


@dataclass(frozen=True)
class EncryptionRequest:
    plaintext: Union[str, bytes]
    aad: Optional[Union[str, bytes]] = None
    algorithm: str = "AES-256-GCM"

    def normalized(self) -> "EncryptionRequest":
        return EncryptionRequest(
            plaintext=_normalize_text(self.plaintext) or "",
            aad=_normalize_text(self.aad),
            algorithm=self.algorithm,
        )


@dataclass(frozen=True)
class EncryptionResponse:
    ciphertext: str
    algorithm: str = "AES-256-GCM"
    aad: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "EncryptionResponse":
        return cls(
            ciphertext=_normalize_ciphertext(data["ciphertext"]) or "",
            algorithm=str(data.get("algorithm", "AES-256-GCM")),
            aad=_normalize_text(data.get("aad")),
        )


@dataclass(frozen=True)
class DecryptionRequest:
    ciphertext: Union[str, bytes]
    aad: Optional[Union[str, bytes]] = None
    algorithm: str = "AES-256-GCM"

    def normalized(self) -> "DecryptionRequest":
        return DecryptionRequest(
            ciphertext=_normalize_ciphertext(self.ciphertext) or "",
            aad=_normalize_text(self.aad),
            algorithm=self.algorithm,
        )


@dataclass(frozen=True)
class DecryptionResponse:
    plaintext: bytes
    algorithm: str = "AES-256-GCM"

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "DecryptionResponse":
        plaintext = data.get("plaintext", b"")
        if isinstance(plaintext, str):
            plaintext = plaintext.encode("utf-8")
        return cls(plaintext=plaintext, algorithm=str(data.get("algorithm", "AES-256-GCM")))
