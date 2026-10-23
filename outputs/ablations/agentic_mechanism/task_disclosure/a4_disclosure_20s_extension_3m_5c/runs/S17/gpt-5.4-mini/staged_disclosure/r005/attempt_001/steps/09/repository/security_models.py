from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Union


JsonDict = Dict[str, Any]


def _coerce_str(value: Any, name: str) -> str:
    if value is None:
        raise ValueError(f"{name} is required")
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    value = value.strip()
    if not value:
        raise ValueError(f"{name} cannot be empty")
    return value


def _coerce_optional_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    value = value.strip()
    return value or None


def _coerce_dict(value: Any, name: str) -> JsonDict:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return dict(value)


def _coerce_list_of_str(value: Any, name: str) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")
    result: List[str] = []
    for item in value:
        result.append(_coerce_str(item, name))
    return result


@dataclass(frozen=True)
class KeyManagementRequest:
    key_id: str
    action: str
    metadata: JsonDict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "KeyManagementRequest":
        return cls(
            key_id=_coerce_str(data.get("key_id"), "key_id"),
            action=_coerce_str(data.get("action"), "action"),
            metadata=_coerce_dict(data.get("metadata"), "metadata"),
        )

    def to_dict(self) -> JsonDict:
        return {"key_id": self.key_id, "action": self.action, "metadata": dict(self.metadata)}


@dataclass(frozen=True)
class KeyManagementResponse:
    key_id: str
    status: str
    details: JsonDict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "KeyManagementResponse":
        return cls(
            key_id=_coerce_str(data.get("key_id"), "key_id"),
            status=_coerce_str(data.get("status"), "status"),
            details=_coerce_dict(data.get("details"), "details"),
        )

    def to_dict(self) -> JsonDict:
        return {"key_id": self.key_id, "status": self.status, "details": dict(self.details)}


@dataclass(frozen=True)
class EncryptionRequest:
    plaintext: str
    key_id: str
    algorithm: str = "aes-256-gcm"
    associated_data: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EncryptionRequest":
        return cls(
            plaintext=_coerce_str(data.get("plaintext"), "plaintext"),
            key_id=_coerce_str(data.get("key_id"), "key_id"),
            algorithm=_coerce_str(data.get("algorithm", "aes-256-gcm"), "algorithm"),
            associated_data=_coerce_optional_str(data.get("associated_data")),
        )

    def to_dict(self) -> JsonDict:
        payload = {"plaintext": self.plaintext, "key_id": self.key_id, "algorithm": self.algorithm}
        if self.associated_data is not None:
            payload["associated_data"] = self.associated_data
        return payload


@dataclass(frozen=True)
class EncryptionResponse:
    ciphertext: str
    key_id: str
    algorithm: str
    iv: Optional[str] = None
    tag: Optional[str] = None
    extra: JsonDict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EncryptionResponse":
        known = {"ciphertext", "key_id", "algorithm", "iv", "tag"}
        extra = {k: v for k, v in data.items() if k not in known}
        return cls(
            ciphertext=_coerce_str(data.get("ciphertext"), "ciphertext"),
            key_id=_coerce_str(data.get("key_id"), "key_id"),
            algorithm=_coerce_str(data.get("algorithm"), "algorithm"),
            iv=_coerce_optional_str(data.get("iv")),
            tag=_coerce_optional_str(data.get("tag")),
            extra=_coerce_dict(extra, "extra"),
        )

    def to_dict(self) -> JsonDict:
        payload = {"ciphertext": self.ciphertext, "key_id": self.key_id, "algorithm": self.algorithm}
        if self.iv is not None:
            payload["iv"] = self.iv
        if self.tag is not None:
            payload["tag"] = self.tag
        payload.update(self.extra)
        return payload


def normalize_key_management_request(value: Union[KeyManagementRequest, Mapping[str, Any]]) -> KeyManagementRequest:
    if isinstance(value, KeyManagementRequest):
        return value
    return KeyManagementRequest.from_dict(value)


def normalize_key_management_response(value: Union[KeyManagementResponse, Mapping[str, Any]]) -> KeyManagementResponse:
    if isinstance(value, KeyManagementResponse):
        return value
    return KeyManagementResponse.from_dict(value)


def normalize_encryption_request(value: Union[EncryptionRequest, Mapping[str, Any]]) -> EncryptionRequest:
    if isinstance(value, EncryptionRequest):
        return value
    return EncryptionRequest.from_dict(value)


def normalize_encryption_response(value: Union[EncryptionResponse, Mapping[str, Any]]) -> EncryptionResponse:
    if isinstance(value, EncryptionResponse):
        return value
    return EncryptionResponse.from_dict(value)
