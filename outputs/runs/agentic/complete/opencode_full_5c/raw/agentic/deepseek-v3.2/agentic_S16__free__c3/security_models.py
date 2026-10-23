from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class SecretProvider(Enum):
    AWS = "aws"
    GCP = "gcp"
    VAULT = "vault"
    AZURE = "azure"


class SecretStatus(Enum):
    ACTIVE = "active"
    PENDING = "pending"
    EXPIRED = "expired"
    DISABLED = "disabled"
    ROTATED = "rotated"


class RotationStage(Enum):
    CURRENT = "AWSCURRENT"
    PENDING = "AWSPENDING"
    PREVIOUS = "AWSPREVIOUS"


@dataclass
class SecretRequest:
    secret_name: str
    provider: SecretProvider
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    project_id: Optional[str] = None
    secret_path: Optional[str] = None
    mount_point: Optional[str] = "secret"

    def validate(self) -> bool:
        if self.provider == SecretProvider.AWS:
            return bool(self.secret_name)
        elif self.provider == SecretProvider.GCP:
            return bool(self.secret_name) and bool(self.project_id)
        elif self.provider == SecretProvider.VAULT:
            return bool(self.secret_path)
        return False


@dataclass
class SecretResponse:
    secret_name: str
    secret_value: Optional[str] = None
    parsed_value: Optional[Dict[str, Any]] = None
    provider: Optional[SecretProvider] = None
    version_id: Optional[str] = None
    version_stages: List[str] = field(default_factory=list)
    status: Optional[SecretStatus] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def is_json(self) -> bool:
        if not self.secret_value:
            return False
        try:
            import json

            json.loads(self.secret_value)
            return True
        except:
            return False

    def parse_json(self) -> Dict[str, Any]:
        if not self.secret_value:
            raise ValueError("No secret value to parse")
        import json

        try:
            self.parsed_value = json.loads(self.secret_value)
            return self.parsed_value
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON secret: {e}") from e


@dataclass
class DatabaseSecret:
    host: str
    port: int
    database: str
    username: str
    password: str
    ssl: bool = False
    ssl_ca: Optional[str] = None
    connection_timeout: int = 30
    max_connections: int = 10

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DatabaseSecret":
        required = ["host", "port", "database", "username", "password"]
        for field in required:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        return cls(
            host=data["host"],
            port=int(data["port"]),
            database=data["database"],
            username=data["username"],
            password=data["password"],
            ssl=data.get("ssl", False),
            ssl_ca=data.get("ssl_ca"),
            connection_timeout=data.get("connection_timeout", 30),
            max_connections=data.get("max_connections", 10),
        )

    def get_connection_string(self) -> str:
        ssl_param = "?ssl=true" if self.ssl else ""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}{ssl_param}"


@dataclass
class RotationInfo:
    secret_name: str
    current_version: Optional[str] = None
    pending_version: Optional[str] = None
    previous_version: Optional[str] = None
    last_rotated: Optional[datetime] = None
    next_rotation: Optional[datetime] = None
    rotation_enabled: bool = False
    rotation_lambda_arn: Optional[str] = None

    def get_status_summary(self) -> Dict[str, Any]:
        return {
            "secret_name": self.secret_name,
            "has_pending": bool(self.pending_version),
            "has_previous": bool(self.previous_version),
            "rotation_enabled": self.rotation_enabled,
            "days_since_last_rotation": (
                (datetime.utcnow() - self.last_rotated).days
                if self.last_rotated
                else None
            ),
        }


@dataclass
class AuditNote:
    secret_name: str
    note: str
    author: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    labels: List[str] = field(default_factory=list)

    def has_sensitive_keywords(self) -> bool:
        sensitive_keywords = ["password", "key", "secret", "token", "credential"]
        note_lower = self.note.lower()
        return any(keyword in note_lower for keyword in sensitive_keywords)
