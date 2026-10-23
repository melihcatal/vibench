from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Mapping, Optional
import base64
import json
import os
import secrets


def _to_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def _normalize_mapping(data: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    return dict(data or {})


def _b64encode_text(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("ascii")


def _b64decode_text(value: str) -> str:
    return base64.b64decode(value.encode("ascii")).decode("utf-8")


def _generate_id(prefix: str) -> str:
    return f"{prefix}_{secrets.token_hex(16)}"


@dataclass(frozen=True)
class KeyManagementRequest:
    key_id: str
    action: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "KeyManagementRequest":
        return cls(
            key_id=_to_str(data.get("key_id") or data.get("id")),
            action=_to_str(data.get("action") or data.get("operation")),
            metadata=_normalize_mapping(data.get("metadata")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"key_id": self.key_id, "action": self.action, "metadata": dict(self.metadata)}


@dataclass(frozen=True)
class KeyManagementResponse:
    key_id: str
    status: str
    details: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "KeyManagementResponse":
        return cls(
            key_id=_to_str(data.get("key_id") or data.get("id")),
            status=_to_str(data.get("status") or data.get("state")),
            details=_normalize_mapping(data.get("details")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"key_id": self.key_id, "status": self.status, "details": dict(self.details)}


@dataclass(frozen=True)
class EncryptionRequest:
    plaintext: str
    key_id: Optional[str] = None
    algorithm: str = "AES-256-GCM"
    associated_data: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EncryptionRequest":
        return cls(
            plaintext=_to_str(data.get("plaintext") or data.get("data") or data.get("message")),
            key_id=(data.get("key_id") or data.get("key")) and _to_str(data.get("key_id") or data.get("key")),
            algorithm=_to_str(data.get("algorithm") or data.get("alg") or "AES-256-GCM"),
            associated_data=(data.get("associated_data") or data.get("aad")) and _to_str(data.get("associated_data") or data.get("aad")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plaintext": self.plaintext,
            "key_id": self.key_id,
            "algorithm": self.algorithm,
            "associated_data": self.associated_data,
        }


@dataclass(frozen=True)
class EncryptionResponse:
    ciphertext: str
    key_id: Optional[str] = None
    algorithm: str = "AES-256-GCM"
    nonce: Optional[str] = None
    tag: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EncryptionResponse":
        return cls(
            ciphertext=_to_str(data.get("ciphertext") or data.get("encrypted") or data.get("payload")),
            key_id=(data.get("key_id") or data.get("key")) and _to_str(data.get("key_id") or data.get("key")),
            algorithm=_to_str(data.get("algorithm") or data.get("alg") or "AES-256-GCM"),
            nonce=(data.get("nonce") or data.get("iv")) and _to_str(data.get("nonce") or data.get("iv")),
            tag=(data.get("tag") or data.get("auth_tag")) and _to_str(data.get("tag") or data.get("auth_tag")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ciphertext": self.ciphertext,
            "key_id": self.key_id,
            "algorithm": self.algorithm,
            "nonce": self.nonce,
            "tag": self.tag,
        }


def normalize_key_management_request(data: Mapping[str, Any]) -> Dict[str, Any]:
    return KeyManagementRequest.from_dict(data).to_dict()


def normalize_key_management_response(data: Mapping[str, Any]) -> Dict[str, Any]:
    return KeyManagementResponse.from_dict(data).to_dict()


def normalize_encryption_request(data: Mapping[str, Any]) -> Dict[str, Any]:
    return EncryptionRequest.from_dict(data).to_dict()


def normalize_encryption_response(data: Mapping[str, Any]) -> Dict[str, Any]:
    return EncryptionResponse.from_dict(data).to_dict()


def create_key_management_request(key_id: str, action: str, metadata: Optional[Mapping[str, Any]] = None) -> KeyManagementRequest:
    return KeyManagementRequest(key_id=key_id, action=action, metadata=_normalize_mapping(metadata))


def create_encryption_request(
    plaintext: str,
    key_id: Optional[str] = None,
    algorithm: str = "AES-256-GCM",
    associated_data: Optional[str] = None,
) -> EncryptionRequest:
    return EncryptionRequest(plaintext=plaintext, key_id=key_id, algorithm=algorithm, associated_data=associated_data)


def encode_ciphertext_bundle(ciphertext: str, nonce: Optional[str] = None, tag: Optional[str] = None) -> str:
    payload = {"ciphertext": ciphertext, "nonce": nonce, "tag": tag}
    return _b64encode_text(json.dumps(payload, separators=(",", ":"), sort_keys=True))


def decode_ciphertext_bundle(bundle: str) -> Dict[str, Any]:
    return json.loads(_b64decode_text(bundle))


def generate_key_identifier(prefix: str = "key") -> str:
    return _generate_id(prefix)


def generate_nonce(length: int = 12) -> str:
    return base64.b64encode(os.urandom(length)).decode("ascii")
