from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass(frozen=True)
class SecretRequest:
    secret_id: str
    region_name: Optional[str] = None


@dataclass(frozen=True)
class SecretResponse:
    secret_id: str
    secret_string: Optional[str] = None
    secret_binary: Optional[bytes] = None
    version_id: Optional[str] = None


@dataclass(frozen=True)
class NormalizedSecret:
    secret_id: str
    value: str
    is_json: bool = False


def normalize_secret_value(secret_id: str, value: Any) -> NormalizedSecret:
    if value is None:
        raise ValueError("Secret value cannot be None")
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    if not isinstance(value, str):
        value = str(value)
    return NormalizedSecret(secret_id=secret_id, value=value, is_json=value.lstrip().startswith("{") and value.rstrip().endswith("}"))


def normalize_secret_response(secret_id: str, response: Mapping[str, Any]) -> NormalizedSecret:
    secret_string = response.get("SecretString")
    if secret_string is not None:
        return normalize_secret_value(secret_id, secret_string)
    secret_binary = response.get("SecretBinary")
    if secret_binary is None:
        raise ValueError("Secret response did not include SecretString or SecretBinary")
    return normalize_secret_value(secret_id, secret_binary)


def build_secret_request(secret_id: str, region_name: Optional[str] = None) -> SecretRequest:
    if not secret_id:
        raise ValueError("secret_id is required")
    return SecretRequest(secret_id=secret_id, region_name=region_name)
