from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SecretState(Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    DESTROYED = "DESTROYED"


@dataclass
class SecretVersion:
    name: str
    secret_id: str
    version_id: str
    state: SecretState
    create_time: Optional[str] = None
    payload: Optional[str] = None

    @classmethod
    def from_metadata(cls, metadata: Dict[str, Any]) -> "SecretVersion":
        parts = metadata["name"].split("/")
        return cls(
            name=metadata["name"],
            secret_id=parts[3],
            version_id=parts[5],
            state=SecretState(metadata["state"]),
            create_time=metadata.get("create_time"),
        )


@dataclass
class SecretRotationSummary:
    secret_id: str
    current_version: str
    previous_version: Optional[str]
    rotation_time: Optional[str]
    versions_count: int
    labels: Dict[str, str]


@dataclass
class SecretSafetyCheck:
    secret_id: str
    is_safe: bool
    unsafe_reasons: list[str]
    labels: Dict[str, str]
    notes: Optional[str]


@dataclass
class SecretAuditEmbedding:
    secret_id: str
    version_id: str
    embedding: list[float]
    audit_text: str
    model_id: str = "textembedding-gecko@latest"
