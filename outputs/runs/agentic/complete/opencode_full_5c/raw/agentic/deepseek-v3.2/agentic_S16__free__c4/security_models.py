from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class SecretStatus(Enum):
    ACTIVE = "active"
    PENDING = "pending"
    EXPIRED = "expired"
    DISABLED = "disabled"
    ROTATING = "rotating"


class SecretType(Enum):
    API_KEY = "api_key"
    DATABASE = "database"
    CERTIFICATE = "certificate"
    SSH_KEY = "ssh_key"
    PASSWORD = "password"
    JSON = "json"
    OTHER = "other"


@dataclass
class SecretMetadata:
    name: str
    type: SecretType
    provider: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    version: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    notes: Optional[str] = None


@dataclass
class SecretResponse:
    success: bool
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[SecretMetadata] = None
    error: Optional[str] = None
    provider_specific: Optional[Dict[str, Any]] = None

    @classmethod
    def from_success(
        cls, data: Dict[str, Any], metadata: SecretMetadata = None
    ) -> "SecretResponse":
        return cls(success=True, data=data, metadata=metadata, error=None)

    @classmethod
    def from_error(
        cls, error: str, metadata: SecretMetadata = None
    ) -> "SecretResponse":
        return cls(success=False, data=None, metadata=metadata, error=error)


@dataclass
class RotationStatus:
    secret_name: str
    current_version: str
    previous_version: Optional[str] = None
    next_rotation_date: Optional[datetime] = None
    last_rotated: Optional[datetime] = None
    rotation_enabled: bool = False
    auto_rotation: bool = False
    status: SecretStatus = SecretStatus.ACTIVE


@dataclass
class AuditEntry:
    timestamp: datetime
    action: str
    secret_name: str
    user: Optional[str] = None
    source_ip: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    success: bool = True


@dataclass
class ValidationResult:
    valid: bool
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_issue(self, issue: str):
        self.issues.append(issue)
        self.valid = False

    def add_warning(self, warning: str):
        self.warnings.append(warning)


class SecretNormalizer:
    """Helper for normalizing secret data across different providers."""

    @staticmethod
    def normalize_db_connection(db_config: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize database connection configuration."""
        normalized = db_config.copy()

        # Ensure standard field names
        field_mapping = {
            "hostname": "host",
            "server": "host",
            "port_number": "port",
            "dbname": "database",
            "db": "database",
            "user": "username",
            "pass": "password",
            "pwd": "password",
        }

        for old_key, new_key in field_mapping.items():
            if old_key in normalized and new_key not in normalized:
                normalized[new_key] = normalized.pop(old_key)

        # Ensure port is integer
        if "port" in normalized and isinstance(normalized["port"], str):
            try:
                normalized["port"] = int(normalized["port"])
            except ValueError:
                pass

        return normalized

    @staticmethod
    def normalize_api_key(api_key_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize API key configuration."""
        normalized = api_key_data.copy()

        # Ensure standard field names
        field_mapping = {
            "key": "api_key",
            "token": "api_key",
            "secret_key": "api_key",
            "access_key": "api_key",
        }

        for old_key, new_key in field_mapping.items():
            if old_key in normalized and new_key not in normalized:
                normalized[new_key] = normalized.pop(old_key)

        return normalized

    @staticmethod
    def extract_common_fields(secret_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract common metadata fields from secret data."""
        common_fields = {}

        metadata_fields = [
            "created",
            "updated",
            "expires",
            "version",
            "description",
            "tags",
        ]
        for field in metadata_fields:
            if field in secret_data:
                common_fields[field] = secret_data[field]

        return common_fields
