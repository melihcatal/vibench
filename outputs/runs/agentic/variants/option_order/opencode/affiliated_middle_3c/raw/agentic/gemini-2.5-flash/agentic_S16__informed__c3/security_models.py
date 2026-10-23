import json
from typing import Any, Dict, Optional


class SecretValue:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value


class SecretRotationStatus:
    def __init__(
        self,
        secret_id: str,
        last_rotation_date: Optional[str] = None,
        next_rotation_date: Optional[str] = None,
        rotation_enabled: bool = False,
    ):
        self.secret_id = secret_id
        self.last_rotation_date = last_rotation_date
        self.next_rotation_date = next_rotation_date
        self.rotation_enabled = rotation_enabled


class SecretMetadata:
    def __init__(
        self,
        secret_id: str,
        labels: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
    ):
        self.secret_id = secret_id
        self.labels = labels if labels is not None else {}
        self.description = description
