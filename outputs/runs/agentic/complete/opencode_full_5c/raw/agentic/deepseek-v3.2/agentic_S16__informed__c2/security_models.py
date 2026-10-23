from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class SecretMetadata:
    """Metadata for a secret."""

    name: str
    arn: str
    description: Optional[str] = None
    created_date: Optional[datetime] = None
    last_accessed_date: Optional[datetime] = None
    last_changed_date: Optional[datetime] = None
    tags: Optional[Dict[str, str]] = None

    @classmethod
    def from_aws_response(cls, response: Dict[str, Any]) -> "SecretMetadata":
        """Create SecretMetadata from AWS DescribeSecret response."""
        return cls(
            name=response.get("Name", ""),
            arn=response.get("ARN", ""),
            description=response.get("Description"),
            created_date=response.get("CreatedDate"),
            last_accessed_date=response.get("LastAccessedDate"),
            last_changed_date=response.get("LastChangedDate"),
            tags=response.get("Tags", {}),
        )


@dataclass
class SecretVersion:
    """Version information for a secret."""

    version_id: str
    version_stages: List[str]
    created_date: Optional[datetime] = None
    last_accessed_date: Optional[datetime] = None

    @classmethod
    def from_aws_response(cls, response: Dict[str, Any]) -> "SecretVersion":
        """Create SecretVersion from AWS ListSecretVersionIds response item."""
        return cls(
            version_id=response.get("VersionId", ""),
            version_stages=response.get("VersionStages", []),
            created_date=response.get("CreatedDate"),
            last_accessed_date=response.get("LastAccessedDate"),
        )


@dataclass
class SecretValue:
    """Secret value with metadata."""

    value: str
    version_id: str
    version_stages: List[str]
    metadata: Optional[SecretMetadata] = None

    @classmethod
    def from_aws_response(
        cls, response: Dict[str, Any], metadata: Optional[SecretMetadata] = None
    ) -> "SecretValue":
        """Create SecretValue from AWS GetSecretValue response."""
        return cls(
            value=response.get("SecretString", ""),
            version_id=response.get("VersionId", ""),
            version_stages=response.get("VersionStages", []),
            metadata=metadata,
        )

    def as_json(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        try:
            return json.loads(self.value)
        except json.JSONDecodeError:
            return {"value": self.value}


@dataclass
class DatabaseConfig:
    """Normalized database configuration."""

    host: str
    port: int
    database: str
    username: str
    password: str
    engine: str = "postgres"

    @classmethod
    def from_secret_data(cls, secret_data: Dict[str, Any]) -> "DatabaseConfig":
        """Create DatabaseConfig from parsed secret data."""
        return cls(
            host=secret_data.get("host") or secret_data.get("endpoint") or "localhost",
            port=int(secret_data.get("port", 5432)),
            database=secret_data.get("database") or secret_data.get("dbname") or "",
            username=secret_data.get("username") or secret_data.get("user") or "",
            password=secret_data.get("password") or "",
            engine=secret_data.get("engine", "postgres"),
        )

    def connection_string(self) -> str:
        """Generate connection string."""
        if self.engine == "postgres":
            return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        elif self.engine == "mysql":
            return f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        else:
            return f"{self.engine}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class RotationStatus:
    """Secret rotation status."""

    secret_name: str
    rotation_enabled: bool
    rotation_lambda_arn: Optional[str] = None
    rotation_rules: Optional[Dict[str, Any]] = None
    last_rotated_date: Optional[datetime] = None
    next_rotation_date: Optional[datetime] = None

    @classmethod
    def from_aws_response(cls, response: Dict[str, Any]) -> "RotationStatus":
        """Create RotationStatus from AWS DescribeSecret response."""
        rotation = response.get("RotationEnabled", False)
        rotation_rules = response.get("RotationRules")

        return cls(
            secret_name=response.get("Name", ""),
            rotation_enabled=rotation,
            rotation_lambda_arn=response.get("RotationLambdaARN"),
            rotation_rules=rotation_rules,
            last_rotated_date=response.get("LastRotatedDate"),
            next_rotation_date=response.get("NextRotationDate"),
        )


class SecretRequest:
    """Request model for secret operations."""

    def __init__(
        self,
        secret_name: str,
        version_id: Optional[str] = None,
        version_stage: Optional[str] = None,
    ):
        self.secret_name = secret_name
        self.version_id = version_id
        self.version_stage = version_stage

    def to_aws_kwargs(self) -> Dict[str, Any]:
        """Convert to kwargs for AWS API calls."""
        kwargs = {"SecretId": self.secret_name}

        if self.version_id:
            kwargs["VersionId"] = self.version_id
        if self.version_stage:
            kwargs["VersionStage"] = self.version_stage

        return kwargs


class SecretResponse:
    """Response model for secret operations."""

    def __init__(
        self,
        success: bool,
        value: Optional[str] = None,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.success = success
        self.value = value
        self.error = error
        self.metadata = metadata or {}

    @classmethod
    def success_response(
        cls, value: str, metadata: Optional[Dict[str, Any]] = None
    ) -> "SecretResponse":
        """Create a success response."""
        return cls(success=True, value=value, metadata=metadata)

    @classmethod
    def error_response(
        cls, error: str, metadata: Optional[Dict[str, Any]] = None
    ) -> "SecretResponse":
        """Create an error response."""
        return cls(success=False, error=error, metadata=metadata)
