from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import base64
import json


def _to_bytes(value: str | bytes) -> bytes:
    if isinstance(value, bytes):
        return value
    return value.encode("utf-8")


def b64encode_text(value: str | bytes) -> str:
    return base64.b64encode(_to_bytes(value)).decode("ascii")


def b64decode_bytes(value: str) -> bytes:
    return base64.b64decode(value.encode("ascii"))


def canonical_json(value: dict[str, Any] | list[Any] | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


@dataclass(slots=True)
class EncryptRequest:
    plaintext: str
    key_id: str
    encryption_context: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class EncryptResponse:
    key_id: str
    ciphertext_b64: str


@dataclass(slots=True)
class DecryptRequest:
    ciphertext_b64: str
    encryption_context: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class DecryptResponse:
    key_id: str
    plaintext: str


@dataclass(slots=True)
class EnvelopeEncryptRequest:
    plaintext: str
    key_id: str
    encryption_context: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class EnvelopeEncryptResponse:
    key_id: str
    wrapped_data_key_b64: str
    ciphertext_b64: str
    nonce_b64: str
    algorithm: str


@dataclass(slots=True)
class SignVerifyRequest:
    key_id: str
    message: str
    signature_b64: str | None = None
    signing_algorithm: str = "RSASSA_PSS_SHA_256"
    action: str = "sign"


@dataclass(slots=True)
class SignVerifyResponse:
    key_id: str
    action: str
    signature_b64: str | None = None
    valid: bool | None = None


@dataclass(slots=True)
class KeyUsageSummary:
    summary: str
    raw_events: list[dict[str, Any]]


@dataclass(slots=True)
class PayloadSafetyResult:
    safe: bool
    category: str
    rationale: str


@dataclass(slots=True)
class EmbeddingResult:
    model: str
    vector: list[float]


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    target_language: str
