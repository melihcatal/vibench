from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretRef:
    project_id: str
    secret_id: str
    version: str = "latest"


@dataclass
class SecretPayload:
    name: str
    value: str
    parsed: Optional[Any] = None


def normalize_secret_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def parse_json_payload(text: str) -> Any:
    import json

    return json.loads(text)


def payload_dict(name: str, value: str, parsed: Optional[Any] = None) -> Dict[str, Any]:
    data = {"name": name, "value": value}
    if parsed is not None:
        data["parsed"] = parsed
    return data
