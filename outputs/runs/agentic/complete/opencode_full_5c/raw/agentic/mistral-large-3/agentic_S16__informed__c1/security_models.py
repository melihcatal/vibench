from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class SecretType(Enum):
    ARBITRARY = "arbitrary"
    PASSWORD = "password"
    CERTIFICATE = "certificate"
    KEY_PAIR = "key_pair"
    USERNAME_PASSWORD = "username_password"


@dataclass
class SecretRequest:
    secret_name: str
    secret_type: SecretType
    description: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    rotation_policy: Optional[Dict[str, Any]] = None


@dataclass
class SecretMetadata:
    name: str
    secret_type: SecretType
    created_at: str
    updated_at: str
    labels: Optional[Dict[str, str]] = None
    version_aliases: Optional[Dict[str, str]] = None


@dataclass
class SecretVersion:
    version_id: str
    secret_value: str
    created_at: str
    state: str


@dataclass
class RotationSummary:
    secret_name: str
    current_version: str
    previous_version: Optional[str]
    rotation_status: str
    last_rotated: Optional[str]
    next_rotation: Optional[str]


def normalize_secret_value(
    secret_value: str, secret_type: SecretType
) -> Dict[str, Any]:
    """
    Normalizes a secret value based on its type.
    """
    if secret_type == SecretType.USERNAME_PASSWORD:
        try:
            username, password = secret_value.split(":", 1)
            return {"username": username, "password": password}
        except ValueError:
            return {"value": secret_value}
    elif secret_type == SecretType.ARBITRARY:
        try:
            return {"value": secret_value}
        except Exception:
            return {"value": secret_value}
    else:
        return {"value": secret_value}
