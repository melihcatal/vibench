import base64
import json
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional, Union


def _coerce_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _maybe_json(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def normalize_bytes_payload(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, Mapping):
        for key in ("plaintext_b64", "ciphertext_b64", "payload_b64", "plaintext", "ciphertext", "payload", "data"):
            if key in value and value[key] is not None:
                return normalize_bytes_payload(value[key])
        raise TypeError("Unsupported payload mapping")
    value = _maybe_json(value)
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        try:
            return base64.b64decode(value, validate=True)
        except Exception:
            return value.encode("utf-8")
    raise TypeError("Unsupported payload type")


def normalize_b64_payload(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("ascii")
    if isinstance(value, Mapping):
        for key in ("plaintext_b64", "ciphertext_b64", "payload_b64"):
            if key in value and value[key] is not None:
                return normalize_b64_payload(value[key])
    raise TypeError("Unsupported payload type")


@dataclass(frozen=True)
class KeyOperationRequest:
    key_name: Optional[str] = None
    payload: Optional[Union[str, bytes, Mapping[str, Any]]] = None

    def normalized_key_name(self, default: Optional[str] = None) -> str:
        key_name = self.key_name or default
        if not key_name:
            raise KeyError("key_name")
        return key_name

    def normalized_payload_bytes(self) -> bytes:
        if self.payload is None:
            raise KeyError("payload")
        return normalize_bytes_payload(self.payload)

    def normalized_payload_b64(self) -> str:
        if self.payload is None:
            raise KeyError("payload")
        return normalize_b64_payload(self.payload)


@dataclass(frozen=True)
class KeyOperationResponse:
    provider: str
    key_name: Optional[str] = None
    plaintext_b64: Optional[str] = None
    plaintext: Optional[str] = None
    ciphertext_b64: Optional[str] = None
    signature_b64: Optional[str] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any], *, provider: str = "unknown") -> "KeyOperationResponse":
        data = dict(value)
        return cls(
            provider=data.get("provider", provider),
            key_name=data.get("key_name"),
            plaintext_b64=data.get("plaintext_b64"),
            plaintext=data.get("plaintext"),
            ciphertext_b64=data.get("ciphertext_b64"),
            signature_b64=data.get("signature_b64") or data.get("Signature"),
            key_id=data.get("key_id") or data.get("KeyId"),
            algorithm=data.get("algorithm") or data.get("encryption_algorithm") or data.get("signing_algorithm"),
            metadata=data,
        )

    def normalized_plaintext(self) -> Optional[str]:
        if self.plaintext is not None:
            return _coerce_text(self.plaintext)
        if self.plaintext_b64 is not None:
            return base64.b64decode(self.plaintext_b64).decode("utf-8", errors="replace")
        return None

    def normalized_plaintext_b64(self) -> Optional[str]:
        if self.plaintext_b64 is not None:
            return self.plaintext_b64
        if self.plaintext is not None:
            return base64.b64encode(_coerce_text(self.plaintext).encode("utf-8")).decode("ascii")
        return None

    def normalized_ciphertext_b64(self) -> Optional[str]:
        if self.ciphertext_b64 is not None:
            return self.ciphertext_b64
        if self.metadata and self.metadata.get("ciphertext") is not None:
            return normalize_b64_payload(self.metadata["ciphertext"])
        return None


def normalize_key_operation_input(value: Any, *, default_key_name: Optional[str] = None) -> KeyOperationRequest:
    if isinstance(value, KeyOperationRequest):
        return value
    if isinstance(value, Mapping):
        return KeyOperationRequest(key_name=value.get("key_name") or default_key_name, payload=value.get("payload") or value)
    return KeyOperationRequest(key_name=default_key_name, payload=value)


def normalize_key_operation_output(value: Any, *, provider: str = "unknown") -> KeyOperationResponse:
    if isinstance(value, KeyOperationResponse):
        return value
    if isinstance(value, Mapping):
        return KeyOperationResponse.from_mapping(value, provider=provider)
    if isinstance(value, bytes):
        return KeyOperationResponse(provider=provider, plaintext_b64=base64.b64encode(value).decode("ascii"), plaintext=value.decode("utf-8", errors="replace"))
    if isinstance(value, str):
        return KeyOperationResponse(provider=provider, plaintext=value, plaintext_b64=base64.b64encode(value.encode("utf-8")).decode("ascii"))
    raise TypeError("Unsupported response type")
