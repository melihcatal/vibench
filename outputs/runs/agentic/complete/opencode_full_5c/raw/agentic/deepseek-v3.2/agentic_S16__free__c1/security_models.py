from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


@dataclass
class SecretRequest:
    """Request model for secret retrieval."""

    secret_name: str
    provider: str
    version: Optional[str] = None
    stage: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary."""
        return {
            "secret_name": self.secret_name,
            "provider": self.provider,
            "version": self.version,
            "stage": self.stage,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SecretRequest":
        """Create request from dictionary."""
        return cls(
            secret_name=data.get("secret_name", ""),
            provider=data.get("provider", ""),
            version=data.get("version"),
            stage=data.get("stage"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class SecretResponse:
    """Response model for secret retrieval."""

    value: Any
    provider: str
    secret_name: str
    version: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    retrieved_at: datetime = field(default_factory=datetime.now)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "value": self.value,
            "provider": self.provider,
            "secret_name": self.secret_name,
            "version": self.version,
            "metadata": self.metadata,
            "retrieved_at": self.retrieved_at.isoformat(),
            "error": self.error,
        }

    def to_safe_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with masked secret value."""
        safe_dict = self.to_dict()
        if self.value:
            if isinstance(self.value, str):
                safe_dict["value"] = "***MASKED***"
            elif isinstance(self.value, dict):
                safe_dict["value"] = {k: "***MASKED***" for k in self.value.keys()}
        return safe_dict


@dataclass
class DatabaseSecret:
    """Model for database connection secrets."""

    host: str
    port: int
    database: str
    username: str
    password: str
    ssl: bool = False
    additional_params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DatabaseSecret":
        """Create database secret from dictionary."""
        return cls(
            host=data["host"],
            port=int(data["port"]),
            database=data["database"],
            username=data["username"],
            password=data["password"],
            ssl=data.get("ssl", False),
            additional_params=data.get("additional_params", {}),
        )

    def get_connection_string(self) -> str:
        """Generate connection string."""
        ssl_param = "?ssl=true" if self.ssl else ""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}{ssl_param}"


@dataclass
class SecretRotationStatus:
    """Model for secret rotation status."""

    secret_name: str
    current_version: str
    pending_version: Optional[str] = None
    previous_version: Optional[str] = None
    last_rotated: Optional[datetime] = None
    rotation_enabled: bool = False
    next_rotation: Optional[datetime] = None
    stages: Dict[str, List[str]] = field(default_factory=dict)

    def is_rotation_in_progress(self) -> bool:
        """Check if rotation is in progress."""
        return self.pending_version is not None

    def get_stage_versions(self, stage: str) -> List[str]:
        """Get versions for a specific stage."""
        return self.stages.get(stage, [])


@dataclass
class SecretAuditNote:
    """Model for secret audit notes."""

    secret_name: str
    note: str
    auditor: str
    timestamp: datetime = field(default_factory=datetime.now)
    labels: List[str] = field(default_factory=list)
    risk_level: str = "low"  # low, medium, high, critical

    def to_embedding_text(self) -> str:
        """Convert to text suitable for embedding."""
        return f"Secret: {self.secret_name}\nNote: {self.note}\nAuditor: {self.auditor}\nRisk: {self.risk_level}\nLabels: {', '.join(self.labels)}"


def normalize_json_secret(data: Any) -> Dict[str, Any]:
    """
    Normalize JSON secret data.

    Args:
        data: Raw JSON data (string or dict)

    Returns:
        Normalized dictionary
    """
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            # If it's not JSON, wrap it
            data = {"raw_value": data}

    if not isinstance(data, dict):
        data = {"value": data}

    # Ensure all values are JSON serializable
    def make_serializable(obj):
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_serializable(item) for item in obj]
        else:
            return str(obj)

    return make_serializable(data)
