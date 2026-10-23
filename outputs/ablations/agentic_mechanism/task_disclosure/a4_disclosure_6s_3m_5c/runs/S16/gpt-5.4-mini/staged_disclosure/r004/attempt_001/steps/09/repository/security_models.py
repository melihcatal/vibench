from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class SecretRequest:
    secret_id: str
    version_id: str = "latest"


@dataclass(frozen=True)
class SecretResponse:
    secret_id: str
    version_id: str
    secret_string: Optional[str] = None
    secret_binary: Optional[bytes] = None
    content_type: Optional[str] = None


def normalize_secret_request(data: Any) -> SecretRequest:
    if isinstance(data, SecretRequest):
        return data
    if isinstance(data, str):
        return SecretRequest(secret_id=data)
    if not isinstance(data, dict):
        raise TypeError("Secret request must be a dict, string, or SecretRequest")
    secret_id = data.get("secret_id") or data.get("secret") or data.get("id")
    if not secret_id:
        raise ValueError("Missing secret_id")
    version_id = data.get("version_id") or data.get("version") or "latest"
    return SecretRequest(secret_id=str(secret_id), version_id=str(version_id))


def normalize_secret_response(data: Any) -> SecretResponse:
    if isinstance(data, SecretResponse):
        return data
    if not isinstance(data, dict):
        raise TypeError("Secret response must be a dict or SecretResponse")
    secret_id = data.get("secret_id") or data.get("secret") or data.get("id")
    version_id = data.get("version_id") or data.get("version") or "latest"
    if not secret_id:
        raise ValueError("Missing secret_id")
    secret_binary = data.get("secret_binary")
    if isinstance(secret_binary, str):
        secret_binary = secret_binary.encode("utf-8")
    return SecretResponse(
        secret_id=str(secret_id),
        version_id=str(version_id),
        secret_string=data.get("secret_string") or data.get("value"),
        secret_binary=secret_binary,
        content_type=data.get("content_type") or data.get("mime_type"),
    )


def request_to_dict(request: SecretRequest) -> Dict[str, Any]:
    return asdict(request)


def response_to_dict(response: SecretResponse) -> Dict[str, Any]:
    payload = asdict(response)
    if payload.get("secret_binary") is not None:
        payload["secret_binary"] = payload["secret_binary"].decode("utf-8", errors="ignore")
    return payload
