from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class SecretMetadata:
    secret_id: str
    arn: str
    name: str
    version_stages: list = field(default_factory=list)
    created_date: Optional[str] = None
    last_accessed_date: Optional[str] = None
    rotation_enabled: bool = False
    rotation_lambda_arn: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "secret_id": self.secret_id,
            "arn": self.arn,
            "name": self.name,
            "version_stages": self.version_stages,
            "created_date": self.created_date,
            "last_accessed_date": self.last_accessed_date,
            "rotation_enabled": self.rotation_enabled,
            "rotation_lambda_arn": self.rotation_lambda_arn,
        }


@dataclass
class SecretResponse:
    secret_value: str
    metadata: SecretMetadata
    provider: str = "AWS Secrets Manager"

    def to_dict(self) -> dict:
        return {
            "secret_value": self.secret_value,
            "metadata": self.metadata.to_dict(),
            "provider": self.provider,
        }


@dataclass
class ParsedSecretResponse:
    secret_value: str
    parsed_data: Dict[str, Any]
    metadata: SecretMetadata
    provider: str = "AWS Secrets Manager"

    def to_dict(self) -> dict:
        return {
            "secret_value": self.secret_value,
            "parsed_data": self.parsed_data,
            "metadata": self.metadata.to_dict(),
            "provider": self.provider,
        }


@dataclass
class RotationStatus:
    secret_name: str
    rotation_enabled: bool
    last_rotated_date: Optional[str]
    next_rotation_date: Optional[str]
    rotation_lambda_arn: Optional[str]
    current_version_id: str
    staged_version_id: Optional[str]
    provider: str = "AWS Secrets Manager"

    def to_dict(self) -> dict:
        return {
            "secret_name": self.secret_name,
            "rotation_enabled": self.rotation_enabled,
            "last_rotated_date": self.last_rotated_date,
            "next_rotation_date": self.next_rotation_date,
            "rotation_lambda_arn": self.rotation_lambda_arn,
            "current_version_id": self.current_version_id,
            "staged_version_id": self.staged_version_id,
            "provider": self.provider,
        }


@dataclass
class LabelSafetyResult:
    label_name: str
    is_safe: bool
    flagged_terms: list = field(default_factory=list)
    severity: str = "none"
    provider: str = "Azure AI Content Safety"

    def to_dict(self) -> dict:
        return {
            "label_name": self.label_name,
            "is_safe": self.is_safe,
            "flagged_terms": self.flagged_terms,
            "severity": self.severity,
            "provider": self.provider,
        }


@dataclass
class EmbeddingResult:
    text: str
    embedding: list
    model: str = "text-embedding-3-small"
    provider: str = "OpenAI Embeddings"

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "embedding": self.embedding,
            "model": self.model,
            "provider": self.provider,
        }


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    provider: str = "DeepL API"

    def to_dict(self) -> dict:
        return {
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "provider": self.provider,
        }
