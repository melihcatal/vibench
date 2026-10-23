import json
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SecretResponse:
    payload: Any

    @classmethod
    def from_google_secret_manager(cls, response: Any) -> "SecretResponse":
        return cls(payload=response.payload.data)

    def as_text(self) -> str:
        if isinstance(self.payload, bytes):
            return self.payload.decode("utf-8")
        return str(self.payload)


def parse_json_payload(raw: str) -> Dict[str, Any]:
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("JSON secret must be an object")
    return data


def normalize_db_secret(raw: str) -> Dict[str, Any]:
    data = parse_json_payload(raw)
    if "uri" not in data and not {"username", "password", "host"}.issubset(data):
        raise ValueError("database secret is missing required fields")
    return data
