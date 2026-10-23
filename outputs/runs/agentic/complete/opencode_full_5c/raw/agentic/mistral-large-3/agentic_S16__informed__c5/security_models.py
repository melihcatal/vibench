from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class SecretType(Enum):
    ARBITRARY = "arbitrary"
    USERNAME_PASSWORD = "username_password"
    IAM_CREDENTIALS = "iam_credentials"
    CERTIFICATE = "certificate"
    KV = "kv"


@dataclass
class SecretVersion:
    version_id: str
    value: str
    created_at: str
    status: str


@dataclass
class SecretMetadata:
    secret_id: str
    name: str
    description: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    versions: Optional[List[SecretVersion]] = None
    rotation_policy: Optional[Dict[str, Any]] = None


@dataclass
class RotationSummary:
    secret_id: str
    current_version: str
    previous_version: Optional[str] = None
    rotation_status: str = "unknown"
    last_rotated: Optional[str] = None
    next_rotation: Optional[str] = None


def normalize_secret_value(value: str, secret_type: SecretType) -> Dict[str, Any]:
    if secret_type == SecretType.KV:
        import json

        return json.loads(value)
    elif secret_type == SecretType.USERNAME_PASSWORD:
        return {"username": value.split(":")[0], "password": value.split(":")[1]}
    return {"value": value}
