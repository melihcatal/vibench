import base64
import json
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union


@dataclass
class SecretFetchRequest:
    secret_name: str
    version: str = "latest"

    def versioned_name(self) -> str:
        if self.version and self.version != "latest":
            return f"{self.secret_name}/versions/{self.version}"
        return self.secret_name


@dataclass
class SecretRotationRequest:
    secret_path: str
    version: Optional[str] = None


@dataclass
class SecretTextResponse:
    value: str


def normalize_secret_payload(payload: Union[str, bytes, Dict[str, Any], Any]) -> Any:
    if isinstance(payload, bytes):
        try:
            return payload.decode("utf-8")
        except UnicodeDecodeError:
            return base64.b64encode(payload).decode("ascii")
    if isinstance(payload, dict):
        return payload
    if hasattr(payload, "decode") and not isinstance(payload, str):
        return payload.decode("utf-8")
    return payload


def parse_json_or_string_secret(value: Union[str, bytes]) -> Any:
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    try:
        return json.loads(value)
    except Exception:
        return {"value": value}


def build_string_payload(value: Any) -> str:
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True)
    return str(value)
