from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum
import json


class SecretType(str, Enum):
    API_KEY = "api_key"
    DATABASE = "database"
    JSON_SECRET = "json_secret"
    VERSIONED = "versioned"


class RotationStatus(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    ROTATED = "rotated"
    EXPIRED = "expired"
    STAGED = "staged"


@dataclass
class VaultConfig:
    address: str = "https://vault.example.com:8200"
    token: str = ""
    namespace: str = ""
    kv_mount: str = "secret"
    api_version: str = "v2"
    timeout: int = 30
    verify_tls: bool = True

    @classmethod
    def from_env(cls) -> "VaultConfig":
        import os

        return cls(
            address=os.environ.get("VAULT_ADDR", "https://vault.example.com:8200"),
            token=os.environ.get("VAULT_TOKEN", ""),
            namespace=os.environ.get("VAULT_NAMESPACE", ""),
            kv_mount=os.environ.get("VAULT_KV_MOUNT", "secret"),
            api_version=os.environ.get("VAULT_API_VERSION", "v2"),
            timeout=int(os.environ.get("VAULT_TIMEOUT", "30")),
            verify_tls=os.environ.get("VAULT_SKIP_VERIFY", "false").lower() != "true",
        )


@dataclass
class SecretRequest:
    secret_path: str
    secret_type: SecretType = SecretType.API_KEY
    version: Optional[int] = None
    field: Optional[str] = None
    mount_point: Optional[str] = None
    namespace: Optional[str] = None


@dataclass
class SecretResponse:
    secret_path: str
    value: Any
    metadata: dict = field(default_factory=dict)
    version: Optional[int] = None
    created_time: Optional[str] = None
    rotation_status: Optional[RotationStatus] = None
    labels: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "secret_path": self.secret_path,
            "value": self.value,
            "metadata": self.metadata,
            "version": self.version,
            "created_time": self.created_time,
            "rotation_status": self.rotation_status.value
            if self.rotation_status
            else None,
            "labels": self.labels,
        }


@dataclass
class RotationSummary:
    secret_path: str
    current_version: int
    previous_version: Optional[int]
    rotation_status: RotationStatus
    last_rotated: Optional[str]
    next_rotation: Optional[str]
    rotation_period_days: Optional[int]
    staged_value: Optional[dict] = None

    def to_dict(self) -> dict:
        return {
            "secret_path": self.secret_path,
            "current_version": self.current_version,
            "previous_version": self.previous_version,
            "rotation_status": self.rotation_status.value,
            "last_rotated": self.last_rotated,
            "next_rotation": self.next_rotation,
            "rotation_period_days": self.rotation_period_days,
            "staged_value": self.staged_value,
        }


@dataclass
class AuditEmbedding:
    secret_path: str
    audit_text: str
    embedding: list[float]
    model: str
    dimensions: int

    def to_dict(self) -> dict:
        return {
            "secret_path": self.secret_path,
            "audit_text": self.audit_text,
            "embedding": self.embedding,
            "model": self.model,
            "dimensions": self.dimensions,
        }


@dataclass
class SafetyCheckResult:
    secret_path: str
    label_name: str
    label_value: str
    is_safe: bool
    categories: dict = field(default_factory=dict)
    flagged_categories: list = field(default_factory=list)
    explanation: str = ""

    def to_dict(self) -> dict:
        return {
            "secret_path": self.secret_path,
            "label_name": self.label_name,
            "label_value": self.label_value,
            "is_safe": self.is_safe,
            "categories": self.categories,
            "flagged_categories": self.flagged_categories,
            "explanation": self.explanation,
        }


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    model: str

    def to_dict(self) -> dict:
        return {
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "model": self.model,
        }


def normalize_vault_response(
    raw_response: dict, secret_path: str, field: Optional[str] = None
) -> SecretResponse:
    data = raw_response.get("data", {})
    secret_data = data.get("data", data)
    metadata = data.get("metadata", {})

    value = secret_data
    if field and isinstance(secret_data, dict):
        value = secret_data.get(field)

    return SecretResponse(
        secret_path=secret_path,
        value=value,
        metadata=metadata,
        version=metadata.get("version"),
        created_time=metadata.get("created_time"),
        labels=secret_data.get("_labels", {}) if isinstance(secret_data, dict) else {},
    )


def parse_json_secret_value(value: Any) -> dict:
    if isinstance(value, str):
        return json.loads(value)
    if isinstance(value, dict):
        return value
    raise ValueError(f"Cannot parse secret value as JSON: {type(value)}")
