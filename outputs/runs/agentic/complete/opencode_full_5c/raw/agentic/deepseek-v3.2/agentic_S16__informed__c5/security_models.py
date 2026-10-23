from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class SecretRequest:
    """Request model for secret operations."""

    secret_name: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    region: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API calls."""
        result = {"SecretId": self.secret_name}
        if self.version_id:
            result["VersionId"] = self.version_id
        if self.version_stage:
            result["VersionStage"] = self.version_stage
        return result


@dataclass
class SecretResponse:
    """Response model for secret retrieval."""

    secret_name: str
    secret_value: str
    version_id: str
    version_stages: List[str]
    created_date: Optional[datetime] = None
    last_accessed_date: Optional[datetime] = None
    last_changed_date: Optional[datetime] = None

    @classmethod
    def from_aws_response(
        cls, secret_name: str, aws_response: Dict[str, Any]
    ) -> "SecretResponse":
        """Create from AWS Secrets Manager response."""
        secret_value = aws_response.get("SecretString", "")
        version_id = aws_response.get("VersionId", "")
        version_stages = aws_response.get("VersionStages", [])

        created_date = aws_response.get("CreatedDate")
        last_accessed_date = aws_response.get("LastAccessedDate")
        last_changed_date = aws_response.get("LastChangedDate")

        return cls(
            secret_name=secret_name,
            secret_value=secret_value,
            version_id=version_id,
            version_stages=version_stages,
            created_date=created_date,
            last_accessed_date=last_accessed_date,
            last_changed_date=last_changed_date,
        )

    def to_json(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        result = {
            "secret_name": self.secret_name,
            "secret_value": self.secret_value,
            "version_id": self.version_id,
            "version_stages": self.version_stages,
        }

        if self.created_date:
            result["created_date"] = self.created_date.isoformat()
        if self.last_accessed_date:
            result["last_accessed_date"] = self.last_accessed_date.isoformat()
        if self.last_changed_date:
            result["last_changed_date"] = self.last_changed_date.isoformat()

        return result


@dataclass
class DatabaseConfig:
    """Normalized database configuration model."""

    host: str
    port: int
    username: str
    password: str
    database: str
    ssl: bool = False
    ssl_ca: Optional[str] = None
    connection_timeout: int = 30
    max_connections: int = 10

    @classmethod
    def from_secret_json(cls, json_data: Dict[str, Any]) -> "DatabaseConfig":
        """Create from parsed JSON secret."""
        return cls(
            host=json_data.get("host", ""),
            port=int(json_data.get("port", 0)),
            username=json_data.get("username", ""),
            password=json_data.get("password", ""),
            database=json_data.get("database", ""),
            ssl=bool(json_data.get("ssl", False)),
            ssl_ca=json_data.get("ssl_ca"),
            connection_timeout=int(json_data.get("connection_timeout", 30)),
            max_connections=int(json_data.get("max_connections", 10)),
        )

    def to_connection_string(self, driver: str = "postgresql") -> str:
        """Generate connection string for common database drivers."""
        if driver == "postgresql":
            ssl_mode = "require" if self.ssl else "disable"
            return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?sslmode={ssl_mode}"
        elif driver == "mysql":
            ssl_param = "&ssl_ca={self.ssl_ca}" if self.ssl and self.ssl_ca else ""
            return f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}{ssl_param}"
        else:
            raise ValueError(f"Unsupported driver: {driver}")


@dataclass
class SecretMetadata:
    """Metadata about a secret."""

    name: str
    arn: str
    description: Optional[str]
    kms_key_id: Optional[str]
    rotation_enabled: bool
    rotation_lambda_arn: Optional[str]
    rotation_rules: Optional[Dict[str, Any]]
    last_rotated_date: Optional[datetime]
    last_changed_date: datetime
    created_date: datetime
    deleted_date: Optional[datetime]
    tags: List[Dict[str, str]]

    @classmethod
    def from_aws_describe(cls, aws_response: Dict[str, Any]) -> "SecretMetadata":
        """Create from AWS describe_secret response."""
        return cls(
            name=aws_response.get("Name", ""),
            arn=aws_response.get("ARN", ""),
            description=aws_response.get("Description"),
            kms_key_id=aws_response.get("KmsKeyId"),
            rotation_enabled=aws_response.get("RotationEnabled", False),
            rotation_lambda_arn=aws_response.get("RotationLambdaARN"),
            rotation_rules=aws_response.get("RotationRules"),
            last_rotated_date=aws_response.get("LastRotatedDate"),
            last_changed_date=aws_response.get("LastChangedDate"),
            created_date=aws_response.get("CreatedDate"),
            deleted_date=aws_response.get("DeletedDate"),
            tags=aws_response.get("Tags", []),
        )


def normalize_secret_value(value: Any) -> str:
    """Normalize secret value to string."""
    if isinstance(value, str):
        return value
    elif isinstance(value, (int, float, bool)):
        return str(value)
    elif isinstance(value, (dict, list)):
        return json.dumps(value)
    else:
        return str(value)
