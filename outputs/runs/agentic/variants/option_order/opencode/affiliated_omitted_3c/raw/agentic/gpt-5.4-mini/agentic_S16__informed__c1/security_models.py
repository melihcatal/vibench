import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class SecretPayload:
    secret_id: str
    value: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


@dataclass(frozen=True)
class JsonSecretPayload:
    secret_id: str
    data: Dict[str, Any]
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


def normalize_secret_response(
    secret_id: str, response: Dict[str, Any]
) -> SecretPayload:
    return SecretPayload(
        secret_id=secret_id,
        value=response.get("SecretString") or response["SecretBinary"].decode("utf-8"),
        version_id=response.get("VersionId"),
        version_stage=(response.get("VersionStages") or [None])[0],
    )


def parse_json_secret(secret_id: str, response: Dict[str, Any]) -> JsonSecretPayload:
    payload = normalize_secret_response(secret_id, response)
    return JsonSecretPayload(
        secret_id=payload.secret_id,
        data=json.loads(payload.value),
        version_id=payload.version_id,
        version_stage=payload.version_stage,
    )
