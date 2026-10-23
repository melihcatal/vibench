import json
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretFetchRequest:
    secret_id: str
    version_stage: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class SecretFetchResponse:
    secret_id: str
    secret_string: Any
    version_id: Optional[str] = None
    version_stages: Optional[list] = None


def normalize_secret_value(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def redact_text(text: str) -> str:
    return re.sub(
        r"(?i)(password|secret|token|key)\s*[:=]\s*[^\s,;]+", r"\1=[REDACTED]", text
    )


def to_response(secret_id: str, response: Dict[str, Any]) -> SecretFetchResponse:
    return SecretFetchResponse(
        secret_id=secret_id,
        secret_string=normalize_secret_value(response.get("SecretString")),
        version_id=response.get("VersionId"),
        version_stages=response.get("VersionStages"),
    )
