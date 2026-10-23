from dataclasses import dataclass, field
from typing import Any, Mapping, Optional
import base64


def _b64decode(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def _b64encode(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def normalize_text(value: Optional[Any]) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def normalize_key_id(value: Optional[Any]) -> Optional[str]:
    text = normalize_text(value)
    if text is None:
        return None
    return text


def normalize_bytes(value: Optional[Any]) -> Optional[bytes]:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            return _b64decode(text)
        except Exception:
            return text.encode("utf-8")
    return str(value).encode("utf-8")


def normalize_bytes_b64(value: Optional[Any]) -> Optional[str]:
    data = normalize_bytes(value)
    if data is None:
        return None
    return _b64encode(data)


def normalize_bool(value: Optional[Any]) -> Optional[bool]:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "y", "on"}:
            return True
        if lowered in {"0", "false", "no", "n", "off"}:
            return False
    return bool(value)


@dataclass(frozen=True)
class KeyReference:
    key_id: Optional[str] = None
    key_arn: Optional[str] = None
    alias_name: Optional[str] = None

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "KeyReference":
        return cls(
            key_id=normalize_key_id(mapping.get("key_id") or mapping.get("KeyId")),
            key_arn=normalize_text(mapping.get("key_arn") or mapping.get("KeyArn")),
            alias_name=normalize_text(mapping.get("alias_name") or mapping.get("AliasName")),
        )


@dataclass(frozen=True)
class EncryptionRequest:
    plaintext: bytes
    key_id: Optional[str] = None
    encryption_context: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "EncryptionRequest":
        return cls(
            plaintext=normalize_bytes(mapping.get("plaintext") or mapping.get("Plaintext")) or b"",
            key_id=normalize_key_id(mapping.get("key_id") or mapping.get("KeyId")),
            encryption_context=dict(mapping.get("encryption_context") or mapping.get("EncryptionContext") or {}),
        )


@dataclass(frozen=True)
class EncryptionResponse:
    ciphertext: bytes
    key_id: Optional[str] = None
    encryption_algorithm: Optional[str] = None
    encryption_context: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "EncryptionResponse":
        return cls(
            ciphertext=normalize_bytes(mapping.get("ciphertext") or mapping.get("CiphertextBlob")) or b"",
            key_id=normalize_key_id(mapping.get("key_id") or mapping.get("KeyId")),
            encryption_algorithm=normalize_text(mapping.get("encryption_algorithm") or mapping.get("EncryptionAlgorithm")),
            encryption_context=dict(mapping.get("encryption_context") or mapping.get("EncryptionContext") or {}),
        )


@dataclass(frozen=True)
class DecryptionRequest:
    ciphertext: bytes
    key_id: Optional[str] = None
    encryption_context: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "DecryptionRequest":
        return cls(
            ciphertext=normalize_bytes(mapping.get("ciphertext") or mapping.get("CiphertextBlob")) or b"",
            key_id=normalize_key_id(mapping.get("key_id") or mapping.get("KeyId")),
            encryption_context=dict(mapping.get("encryption_context") or mapping.get("EncryptionContext") or {}),
        )


@dataclass(frozen=True)
class DecryptionResponse:
    plaintext: bytes
    key_id: Optional[str] = None
    encryption_algorithm: Optional[str] = None

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "DecryptionResponse":
        return cls(
            plaintext=normalize_bytes(mapping.get("plaintext") or mapping.get("Plaintext")) or b"",
            key_id=normalize_key_id(mapping.get("key_id") or mapping.get("KeyId")),
            encryption_algorithm=normalize_text(mapping.get("encryption_algorithm") or mapping.get("EncryptionAlgorithm")),
        )


@dataclass(frozen=True)
class SignRequest:
    message: bytes
    key_id: Optional[str] = None
    message_type: Optional[str] = None
    signing_algorithm: Optional[str] = None

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "SignRequest":
        return cls(
            message=normalize_bytes(mapping.get("message") or mapping.get("Message")) or b"",
            key_id=normalize_key_id(mapping.get("key_id") or mapping.get("KeyId")),
            message_type=normalize_text(mapping.get("message_type") or mapping.get("MessageType")),
            signing_algorithm=normalize_text(mapping.get("signing_algorithm") or mapping.get("SigningAlgorithm")),
        )


@dataclass(frozen=True)
class VerifyRequest:
    message: bytes
    signature: bytes
    key_id: Optional[str] = None
    message_type: Optional[str] = None
    signing_algorithm: Optional[str] = None

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "VerifyRequest":
        return cls(
            message=normalize_bytes(mapping.get("message") or mapping.get("Message")) or b"",
            signature=normalize_bytes(mapping.get("signature") or mapping.get("Signature")) or b"",
            key_id=normalize_key_id(mapping.get("key_id") or mapping.get("KeyId")),
            message_type=normalize_text(mapping.get("message_type") or mapping.get("MessageType")),
            signing_algorithm=normalize_text(mapping.get("signing_algorithm") or mapping.get("SigningAlgorithm")),
        )


@dataclass(frozen=True)
class EnvelopeEncryptionResult:
    ciphertext: bytes
    encrypted_data_key: bytes
    key_id: Optional[str] = None
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "EnvelopeEncryptionResult":
        return cls(
            ciphertext=normalize_bytes(mapping.get("ciphertext") or mapping.get("Ciphertext")) or b"",
            encrypted_data_key=normalize_bytes(mapping.get("encrypted_data_key") or mapping.get("EncryptedDataKey")) or b"",
            key_id=normalize_key_id(mapping.get("key_id") or mapping.get("KeyId")),
            iv=normalize_bytes(mapping.get("iv") or mapping.get("Iv")),
            tag=normalize_bytes(mapping.get("tag") or mapping.get("Tag")),
        )
