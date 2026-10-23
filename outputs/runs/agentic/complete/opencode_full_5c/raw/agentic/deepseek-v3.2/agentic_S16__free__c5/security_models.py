from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
import json


class SecretType(Enum):
    """Types of secrets."""

    API_KEY = "api_key"
    DATABASE = "database"
    SSH_KEY = "ssh_key"
    TLS_CERT = "tls_cert"
    PASSWORD = "password"
    JSON = "json"
    BINARY = "binary"
    OTHER = "other"


class RotationStatus(Enum):
    """Secret rotation status."""

    ACTIVE = "active"
    PENDING = "pending"
    FAILED = "failed"
    DISABLED = "disabled"
    SCHEDULED = "scheduled"


class SecretPriority(Enum):
    """Secret priority levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class SecretMetadata:
    """Metadata for a secret."""

    created_at: datetime
    updated_at: datetime
    version: str
    rotation_enabled: bool = False
    last_rotated: Optional[datetime] = None
    next_rotation: Optional[datetime] = None
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with ISO format dates."""
        result = {
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version,
            "rotation_enabled": self.rotation_enabled,
            "labels": self.labels,
            "annotations": self.annotations,
        }
        if self.last_rotated:
            result["last_rotated"] = self.last_rotated.isoformat()
        if self.next_rotation:
            result["next_rotation"] = self.next_rotation.isoformat()
        return result


@dataclass
class SecretRequest:
    """Request model for fetching secrets."""

    name: str
    version: Optional[str] = None
    version_stage: Optional[str] = None
    project_id: Optional[str] = None
    vault_url: Optional[str] = None
    timeout: int = 30

    def validate(self) -> List[str]:
        """Validate request parameters."""
        errors = []
        if not self.name or len(self.name) > 256:
            errors.append("Secret name must be 1-256 characters")
        if self.version and self.version_stage:
            errors.append("Cannot specify both version and version_stage")
        return errors


@dataclass
class SecretResponse:
    """Response model for secret operations."""

    success: bool
    name: str
    value: Optional[str] = None
    parsed_value: Optional[Any] = None
    metadata: Optional[SecretMetadata] = None
    secret_type: SecretType = SecretType.OTHER
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)

    def to_safe_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with masked sensitive data."""
        result = {
            "success": self.success,
            "name": self.name,
            "secret_type": self.secret_type.value,
            "warnings": self.warnings,
        }

        if self.metadata:
            result["metadata"] = self.metadata.to_dict()

        if self.error:
            result["error"] = self.error

        # Never include actual secret value in safe dict
        if self.value:
            result["has_value"] = True
            result["value_length"] = len(self.value)
        else:
            result["has_value"] = False

        return result


@dataclass
class RotationRequest:
    """Request model for secret rotation."""

    secret_name: str
    new_value: Optional[str] = None
    auto_generate: bool = False
    length: int = 32
    include_special_chars: bool = True
    rotation_reason: Optional[str] = None
    schedule_rotation: bool = False
    rotation_date: Optional[datetime] = None

    def validate(self) -> List[str]:
        """Validate rotation request."""
        errors = []
        if not self.secret_name:
            errors.append("Secret name is required")
        if not self.new_value and not self.auto_generate:
            errors.append("Either new_value or auto_generate must be specified")
        if self.auto_generate and self.length < 8:
            errors.append("Generated password must be at least 8 characters")
        return errors


@dataclass
class RotationResult:
    """Result model for rotation operations."""

    success: bool
    secret_name: str
    old_version: Optional[str] = None
    new_version: Optional[str] = None
    rotation_status: RotationStatus = RotationStatus.ACTIVE
    scheduled_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "success": self.success,
            "secret_name": self.secret_name,
            "rotation_status": self.rotation_status.value,
        }

        if self.old_version:
            result["old_version"] = self.old_version
        if self.new_version:
            result["new_version"] = self.new_version
        if self.scheduled_time:
            result["scheduled_time"] = self.scheduled_time.isoformat()
        if self.completion_time:
            result["completion_time"] = self.completion_time.isoformat()
        if self.error:
            result["error"] = self.error

        return result


@dataclass
class AuditEntry:
    """Audit log entry for secret operations."""

    timestamp: datetime
    operation: str
    secret_name: str
    user: Optional[str] = None
    source_ip: Optional[str] = None
    success: bool = True
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "operation": self.operation,
            "secret_name": self.secret_name,
            "user": self.user,
            "source_ip": self.source_ip,
            "success": self.success,
            "details": self.details,
        }


class SecretNormalizer:
    """Helper for normalizing secret data across providers."""

    @staticmethod
    def normalize_database_secret(secret_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize database connection secrets to standard format."""
        normalized = {}

        # Map common field names
        field_mapping = {
            "hostname": "host",
            "host_name": "host",
            "server": "host",
            "port_number": "port",
            "db": "database",
            "db_name": "database",
            "dbname": "database",
            "user": "username",
            "user_name": "username",
            "pass": "password",
            "passwd": "password",
            "pwd": "password",
        }

        for key, value in secret_data.items():
            normalized_key = field_mapping.get(key.lower(), key)
            normalized[normalized_key] = value

        # Ensure standard fields exist
        standard_fields = ["host", "port", "database", "username", "password"]
        for field in standard_fields:
            if field not in normalized:
                normalized[field] = None

        # Convert port to integer if possible
        if normalized["port"] and isinstance(normalized["port"], str):
            try:
                normalized["port"] = int(normalized["port"])
            except ValueError:
                pass

        return normalized

    @staticmethod
    def normalize_api_key_secret(secret_data: Any) -> Dict[str, Any]:
        """Normalize API key secrets."""
        if isinstance(secret_data, dict):
            return secret_data
        elif isinstance(secret_data, str):
            # Try to parse as JSON
            try:
                parsed = json.loads(secret_data)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass

            # Treat as simple API key
            return {"api_key": secret_data}
        else:
            return {"value": str(secret_data)}

    @staticmethod
    def extract_secret_type(
        secret_data: Any, content_type: Optional[str] = None
    ) -> SecretType:
        """Determine secret type from content."""
        if content_type == "application/json":
            return SecretType.JSON

        if isinstance(secret_data, dict):
            keys_lower = [k.lower() for k in secret_data.keys()]
            if any(db_key in keys_lower for db_key in ["host", "database", "port"]):
                return SecretType.DATABASE
            elif any(
                api_key in keys_lower for api_key in ["api_key", "apikey", "token"]
            ):
                return SecretType.API_KEY
            elif any(
                ssh_key in keys_lower
                for ssh_key in ["private_key", "public_key", "ssh"]
            ):
                return SecretType.SSH_KEY
            else:
                return SecretType.JSON

        if isinstance(secret_data, str):
            if (
                "BEGIN PRIVATE KEY" in secret_data
                or "BEGIN RSA PRIVATE KEY" in secret_data
            ):
                return SecretType.SSH_KEY
            elif "BEGIN CERTIFICATE" in secret_data:
                return SecretType.TLS_CERT
            elif (
                len(secret_data) <= 100
                and "=" not in secret_data
                and "\n" not in secret_data
            ):
                return SecretType.PASSWORD

        return SecretType.OTHER
