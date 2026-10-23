from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional
import base64
import binascii
import re


_WS_RE = re.compile(r"\s+")


def _strip_text(value: Optional[str]) -> str:
    return _WS_RE.sub(" ", (value or "")).strip()


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _coerce_bytes(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return b""
        try:
            return base64.b64decode(text, validate=True)
        except (binascii.Error, ValueError):
            return text.encode("utf-8")
    raise TypeError(f"Unsupported bytes value type: {type(value)!r}")


def _b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _b64decode(text: str) -> bytes:
    return base64.b64decode(text.encode("ascii"), validate=True)


def normalize_key_id(value: Optional[str]) -> str:
    return _strip_text(value)


def normalize_plaintext(value: Optional[str]) -> str:
    return value or ""


def normalize_ciphertext(value: Optional[str]) -> str:
    return _strip_text(value)


def normalize_algorithm(value: Optional[str]) -> str:
    return _strip_text(value).upper()


@dataclass(frozen=True)
class KeyOperationRequest:
    key_id: str
    algorithm: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)
    requested_at: datetime = field(default_factory=_utc_now)

    def normalized(self) -> "KeyOperationRequest":
        return KeyOperationRequest(
            key_id=normalize_key_id(self.key_id),
            algorithm=normalize_algorithm(self.algorithm),
            metadata=dict(self.metadata),
            requested_at=self.requested_at.astimezone(timezone.utc),
        )


@dataclass(frozen=True)
class EncryptPayloadRequest(KeyOperationRequest):
    plaintext: str = ""

    def normalized(self) -> "EncryptPayloadRequest":
        base = super().normalized()
        return EncryptPayloadRequest(
            key_id=base.key_id,
            algorithm=base.algorithm,
            metadata=base.metadata,
            requested_at=base.requested_at,
            plaintext=normalize_plaintext(self.plaintext),
        )


@dataclass(frozen=True)
class DecryptPayloadRequest(KeyOperationRequest):
    ciphertext: str = ""

    def normalized(self) -> "DecryptPayloadRequest":
        base = super().normalized()
        return DecryptPayloadRequest(
            key_id=base.key_id,
            algorithm=base.algorithm,
            metadata=base.metadata,
            requested_at=base.requested_at,
            ciphertext=normalize_ciphertext(self.ciphertext),
        )


@dataclass(frozen=True)
class SignRequest(KeyOperationRequest):
    message: str = ""

    def normalized(self) -> "SignRequest":
        base = super().normalized()
        return SignRequest(
            key_id=base.key_id,
            algorithm=base.algorithm,
            metadata=base.metadata,
            requested_at=base.requested_at,
            message=normalize_plaintext(self.message),
        )


@dataclass(frozen=True)
class VerifyRequest(SignRequest):
    signature: str = ""

    def normalized(self) -> "VerifyRequest":
        base = super().normalized()
        return VerifyRequest(
            key_id=base.key_id,
            algorithm=base.algorithm,
            metadata=base.metadata,
            requested_at=base.requested_at,
            message=base.message,
            signature=normalize_ciphertext(self.signature),
        )


@dataclass(frozen=True)
class OperationResponse:
    ok: bool = False
    request_id: str = ""
    key_id: str = ""
    algorithm: str = ""
    created_at: datetime = field(default_factory=_utc_now)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def normalized(self) -> "OperationResponse":
        return OperationResponse(
            ok=bool(self.ok),
            request_id=_strip_text(self.request_id),
            key_id=normalize_key_id(self.key_id),
            algorithm=normalize_algorithm(self.algorithm),
            created_at=self.created_at.astimezone(timezone.utc),
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class EncryptPayloadResponse(OperationResponse):
    ciphertext: str = ""
    plaintext_sha256: str = ""

    def normalized(self) -> "EncryptPayloadResponse":
        base = super().normalized()
        return EncryptPayloadResponse(
            ok=base.ok,
            request_id=base.request_id,
            key_id=base.key_id,
            algorithm=base.algorithm,
            created_at=base.created_at,
            metadata=base.metadata,
            ciphertext=normalize_ciphertext(self.ciphertext),
            plaintext_sha256=_strip_text(self.plaintext_sha256).lower(),
        )


@dataclass(frozen=True)
class DecryptPayloadResponse(OperationResponse):
    plaintext: str = ""
    payload_len: int = 0

    def normalized(self) -> "DecryptPayloadResponse":
        base = super().normalized()
        return DecryptPayloadResponse(
            ok=base.ok,
            request_id=base.request_id,
            key_id=base.key_id,
            algorithm=base.algorithm,
            created_at=base.created_at,
            metadata=base.metadata,
            plaintext=normalize_plaintext(self.plaintext),
            payload_len=max(0, int(self.payload_len)),
        )


@dataclass(frozen=True)
class SignResponse(OperationResponse):
    signature: str = ""

    def normalized(self) -> "SignResponse":
        base = super().normalized()
        return SignResponse(
            ok=base.ok,
            request_id=base.request_id,
            key_id=base.key_id,
            algorithm=base.algorithm,
            created_at=base.created_at,
            metadata=base.metadata,
            signature=normalize_ciphertext(self.signature),
        )


@dataclass(frozen=True)
class VerifyResponse(OperationResponse):
    verified: bool = False

    def normalized(self) -> "VerifyResponse":
        base = super().normalized()
        return VerifyResponse(
            ok=base.ok,
            request_id=base.request_id,
            key_id=base.key_id,
            algorithm=base.algorithm,
            created_at=base.created_at,
            metadata=base.metadata,
            verified=bool(self.verified),
        )


@dataclass(frozen=True)
class EnvelopeKeyMaterial:
    kek_key_id: str = ""
    encrypted_data_key: str = ""
    data_key: bytes = b""

    def normalized(self) -> "EnvelopeKeyMaterial":
        return EnvelopeKeyMaterial(
            kek_key_id=normalize_key_id(self.kek_key_id),
            encrypted_data_key=normalize_ciphertext(self.encrypted_data_key),
            data_key=_coerce_bytes(self.data_key),
        )


@dataclass(frozen=True)
class EnvelopeEncryptRequest(KeyOperationRequest):
    plaintext: str = ""
    aad: str = ""

    def normalized(self) -> "EnvelopeEncryptRequest":
        base = super().normalized()
        return EnvelopeEncryptRequest(
            key_id=base.key_id,
            algorithm=base.algorithm,
            metadata=base.metadata,
            requested_at=base.requested_at,
            plaintext=normalize_plaintext(self.plaintext),
            aad=normalize_plaintext(self.aad),
        )


@dataclass(frozen=True)
class EnvelopeEncryptResponse(OperationResponse):
    encrypted_data_key: str = ""
    ciphertext: str = ""

    def normalized(self) -> "EnvelopeEncryptResponse":
        base = super().normalized()
        return EnvelopeEncryptResponse(
            ok=base.ok,
            request_id=base.request_id,
            key_id=base.key_id,
            algorithm=base.algorithm,
            created_at=base.created_at,
            metadata=base.metadata,
            encrypted_data_key=normalize_ciphertext(self.encrypted_data_key),
            ciphertext=normalize_ciphertext(self.ciphertext),
        )


def decode_b64_field(value: Optional[str]) -> bytes:
    text = _strip_text(value)
    return b"" if not text else _b64decode(text)


def encode_b64_field(value: Any) -> str:
    return _b64encode(_coerce_bytes(value))


def coerce_request(data: Mapping[str, Any], request_type: type[KeyOperationRequest]) -> KeyOperationRequest:
    return request_type(**dict(data)).normalized()


def response_from_mapping(data: Mapping[str, Any], response_type: type[OperationResponse]) -> OperationResponse:
    return response_type(**dict(data)).normalized()
