from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SecretRequest:
    secret_id: str
    version_stage: str = "AWSCURRENT"
    version_id: Optional[str] = None
    client_request_token: Optional[str] = None


@dataclass
class SecretResponse:
    secret_id: str
    secret_value: str
    version_id: str
    version_stage: str
    arn: str
    provider: str = "aws-secrets-manager"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def model_dump(self) -> Dict[str, Any]:
        return {
            "secret_id": self.secret_id,
            "secret_value": self.secret_value,
            "version_id": self.version_id,
            "version_stage": self.version_stage,
            "arn": self.arn,
            "provider": self.provider,
            "metadata": self.metadata,
        }


@dataclass
class RotationStatus:
    secret_id: str
    rotation_enabled: bool
    last_rotated_date: Optional[str] = None
    next_rotation_date: Optional[str] = None
    rotation_lambda_arn: Optional[str] = None
    current_version: Optional[str] = None
    pending_version: Optional[str] = None

    def model_dump(self) -> Dict[str, Any]:
        return {
            "secret_id": self.secret_id,
            "rotation_enabled": self.rotation_enabled,
            "last_rotated_date": self.last_rotated_date,
            "next_rotation_date": self.next_rotation_date,
            "rotation_lambda_arn": self.rotation_lambda_arn,
            "current_version": self.current_version,
            "pending_version": self.pending_version,
        }


@dataclass
class AuditNote:
    secret_id: str
    note_text: str
    timestamp: str
    author: str = ""
    labels: List[str] = field(default_factory=list)

    def model_dump(self) -> Dict[str, Any]:
        return {
            "secret_id": self.secret_id,
            "note_text": self.note_text,
            "timestamp": self.timestamp,
            "author": self.author,
            "labels": self.labels,
        }


@dataclass
class RunbookEntry:
    entry_id: str
    title: str
    content: str
    source_language: str = "en"
    target_language: str = "ja"

    def model_dump(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "title": self.title,
            "content": self.content,
            "source_language": self.source_language,
            "target_language": self.target_language,
        }
