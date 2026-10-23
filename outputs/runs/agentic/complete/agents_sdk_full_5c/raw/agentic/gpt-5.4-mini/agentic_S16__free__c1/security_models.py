from __future__ import annotations

import base64
import json
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping


@dataclass
class SecretFetchResult:
    secret_id: str
    version_id: str | None
    value: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecretRequest:
    secret_id: str
    version_stage: str | None = None


@dataclass
class SecretResponse:
    secret_id: str
    version_id: str | None
    data: Dict[str, Any]


def normalize_secret_payload(response: Mapping[str, Any]) -> Dict[str, Any]:
    if "SecretString" in response and response["SecretString"] is not None:
        secret_string = response["SecretString"]
        try:
            return json.loads(secret_string)
        except Exception:
            return {"secret_string": secret_string}
    if "SecretBinary" in response and response["SecretBinary"] is not None:
        decoded = base64.b64decode(response["SecretBinary"])
        try:
            return json.loads(decoded.decode("utf-8"))
        except Exception:
            return {"secret_binary": decoded.decode("utf-8", errors="replace")}
    return {k: v for k, v in response.items() if k not in {"ARN", "Name", "VersionId", "CreatedDate"}}
