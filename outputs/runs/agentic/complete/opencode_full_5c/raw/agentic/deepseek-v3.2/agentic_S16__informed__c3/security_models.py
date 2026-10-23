from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class SecretMetadata:
    """Model for secret metadata."""

    name: str
    arn: str
    description: Optional[str] = None
    last_accessed_date: Optional[datetime] = None
    last_changed_date: Optional[datetime] = None
    last_rotated_date: Optional[datetime] = None
    rotation_enabled: bool = False
    rotation_lambda_arn: Optional[str] = None
    rotation_rules: Optional[Dict[str, Any]] = None
    tags: Optional[List[Dict[str, str]]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with ISO format dates."""
        result = asdict(self)
        # Convert datetime objects to ISO strings
        for field in ["last_accessed_date", "last_changed_date", "last_rotated_date"]:
            if result[field] and isinstance(result[field], datetime):
                result[field] = result[field].isoformat()
        return result


@dataclass
class SecretVersion:
    """Model for secret version information."""

    version_id: str
    version_stages: List[str]
    created_date: datetime
    secret_value: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "version_id": self.version_id,
            "version_stages": self.version_stages,
            "created_date": self.created_date.isoformat(),
            "secret_value": self.secret_value,
        }


@dataclass
class DatabaseSecret:
    """Normalized database connection secret model."""

    host: str
    port: int
    database: str
    username: str
    password: str
    engine: str = "postgres"
    ssl: bool = True
    ssl_mode: str = "require"

    @classmethod
    def from_raw_secret(cls, raw_secret: Dict[str, Any]) -> "DatabaseSecret":
        """Create from raw secret dictionary with field normalization."""
        # Map common field names
        field_map = {
            "host": ["host", "endpoint", "server", "hostname"],
            "port": ["port"],
            "database": ["database", "dbname", "db", "name"],
            "username": ["username", "user", "login"],
            "password": ["password", "pass", "passwd"],
            "engine": ["engine", "type", "dbms"],
        }

        normalized = {}
        for target_field, source_fields in field_map.items():
            value = None
            for source_field in source_fields:
                if source_field in raw_secret:
                    value = raw_secret[source_field]
                    break

            if value is None and target_field in [
                "host",
                "database",
                "username",
                "password",
            ]:
                raise ValueError(f"Missing required field: {target_field}")

            normalized[target_field] = value

        # Convert port to int
        if normalized.get("port"):
            try:
                normalized["port"] = int(normalized["port"])
            except (ValueError, TypeError):
                normalized["port"] = 5432

        return cls(**normalized)

    def connection_string(self) -> str:
        """Generate connection string for common databases."""
        if self.engine.lower() == "postgres":
            ssl_part = "sslmode=require" if self.ssl else ""
            return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?{ssl_part}"
        elif self.engine.lower() == "mysql":
            ssl_part = "ssl-mode=REQUIRED" if self.ssl else ""
            return f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?{ssl_part}"
        else:
            return f"{self.engine}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class ApiKeySecret:
    """Model for API key secrets."""

    api_key: str
    key_id: Optional[str] = None
    key_name: Optional[str] = None
    environment: Optional[str] = None
    expires_at: Optional[datetime] = None

    @classmethod
    def from_raw_secret(cls, raw_secret: Any) -> "ApiKeySecret":
        """Create from raw secret (string or dict)."""
        if isinstance(raw_secret, str):
            return cls(api_key=raw_secret)
        elif isinstance(raw_secret, dict):
            return cls(
                api_key=raw_secret.get("api_key", raw_secret.get("key", "")),
                key_id=raw_secret.get("key_id"),
                key_name=raw_secret.get("key_name", raw_secret.get("name")),
                environment=raw_secret.get("environment", raw_secret.get("env")),
                expires_at=raw_secret.get("expires_at"),
            )
        else:
            raise ValueError(f"Unsupported secret type: {type(raw_secret)}")


class SecretNormalizer:
    """Utility for normalizing secret data."""

    @staticmethod
    def normalize_json_secret(secret_string: str) -> Dict[str, Any]:
        """Parse and normalize JSON secret."""
        try:
            data = json.loads(secret_string)
            if isinstance(data, dict):
                return data
            elif isinstance(data, list):
                return {"items": data}
            else:
                return {"value": data}
        except json.JSONDecodeError:
            # If not JSON, treat as plain text
            return {"value": secret_string}

    @staticmethod
    def extract_rotation_status(secret_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Extract rotation status from secret metadata."""
        return {
            "rotation_enabled": secret_metadata.get("RotationEnabled", False),
            "last_rotated_date": secret_metadata.get("LastRotatedDate"),
            "next_rotation_date": secret_metadata.get("NextRotationDate"),
            "rotation_lambda_arn": secret_metadata.get("RotationLambdaARN"),
            "rotation_rules": secret_metadata.get("RotationRules", {}),
        }

    @staticmethod
    def validate_secret_value(value: Any, secret_type: str = "generic") -> bool:
        """Validate secret value based on type."""
        if not value:
            return False

        if secret_type == "api_key":
            return isinstance(value, str) and len(value.strip()) > 0
        elif secret_type == "database":
            return isinstance(value, dict) and all(
                key in value for key in ["host", "database", "username", "password"]
            )
        elif secret_type == "json":
            try:
                json.loads(value if isinstance(value, str) else json.dumps(value))
                return True
            except (json.JSONDecodeError, TypeError):
                return False
        else:
            return True
