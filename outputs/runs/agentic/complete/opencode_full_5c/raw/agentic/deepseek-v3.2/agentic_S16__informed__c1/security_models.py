from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class SecretRequest:
    """Request model for secret operations."""

    name: str
    version_stage: Optional[str] = None
    version_id: Optional[str] = None
    region: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API calls."""
        result = {"SecretId": self.name}
        if self.version_stage:
            result["VersionStage"] = self.version_stage
        if self.version_id:
            result["VersionId"] = self.version_id
        return result


@dataclass
class SecretResponse:
    """Response model for secret data."""

    name: str
    value: Optional[str] = None
    binary_value: Optional[bytes] = None
    version_id: Optional[str] = None
    version_stages: List[str] = None
    created_date: Optional[datetime] = None
    arn: Optional[str] = None
    rotation_enabled: bool = False

    def __post_init__(self):
        if self.version_stages is None:
            self.version_stages = []

    @classmethod
    def from_aws_response(cls, response: Dict[str, Any]) -> "SecretResponse":
        """Create from AWS Secrets Manager response."""
        value = None
        binary_value = None

        if "SecretString" in response:
            value = response["SecretString"]
        elif "SecretBinary" in response:
            binary_value = response["SecretBinary"]

        return cls(
            name=response.get("Name", ""),
            value=value,
            binary_value=binary_value,
            version_id=response.get("VersionId"),
            version_stages=response.get("VersionStages", []),
            created_date=response.get("CreatedDate"),
            arn=response.get("ARN"),
            rotation_enabled=response.get("RotationEnabled", False),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "value": self.value,
            "has_binary": self.binary_value is not None,
            "version_id": self.version_id,
            "version_stages": self.version_stages,
            "created_date": self.created_date.isoformat()
            if self.created_date
            else None,
            "arn": self.arn,
            "rotation_enabled": self.rotation_enabled,
        }


@dataclass
class DatabaseSecret:
    """Model for database connection secrets."""

    host: str
    port: int
    database: str
    username: str
    password: str
    engine: Optional[str] = None
    ssl: bool = False

    @classmethod
    def from_json(cls, json_data: str) -> "DatabaseSecret":
        """Create from JSON string."""
        data = json.loads(json_data)
        return cls(
            host=data.get("host", ""),
            port=int(data.get("port", 0)),
            database=data.get("database") or data.get("dbname", ""),
            username=data.get("username", ""),
            password=data.get("password", ""),
            engine=data.get("engine"),
            ssl=data.get("ssl", False),
        )

    def connection_string(self) -> str:
        """Generate connection string."""
        if self.engine == "postgres":
            ssl_mode = "?sslmode=require" if self.ssl else ""
            return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}{ssl_mode}"
        elif self.engine == "mysql":
            ssl_flag = "&ssl-mode=REQUIRED" if self.ssl else ""
            return f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}{ssl_flag}"
        else:
            return f"{self.engine}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class RotationStatus:
    """Model for secret rotation status."""

    secret_name: str
    rotation_enabled: bool
    rotation_lambda_arn: Optional[str] = None
    rotation_rules: Optional[Dict[str, Any]] = None
    last_rotated_date: Optional[datetime] = None
    last_changed_date: Optional[datetime] = None
    next_rotation_date: Optional[datetime] = None

    @classmethod
    def from_aws_response(cls, response: Dict[str, Any]) -> "RotationStatus":
        """Create from AWS describe_secret response."""
        return cls(
            secret_name=response.get("Name", ""),
            rotation_enabled=response.get("RotationEnabled", False),
            rotation_lambda_arn=response.get("RotationLambdaARN"),
            rotation_rules=response.get("RotationRules"),
            last_rotated_date=response.get("LastRotatedDate"),
            last_changed_date=response.get("LastChangedDate"),
            next_rotation_date=response.get("NextRotationDate"),
        )


def parse_json_secret_data(json_string: str) -> Dict[str, Any]:
    """Parse JSON secret data with error handling."""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in secret: {e}")


def validate_secret_name(name: str) -> bool:
    """Validate secret name format."""
    if not name:
        return False
    if len(name) > 256:
        return False
    # AWS Secrets Manager names can contain letters, numbers, and these characters: /_+=.@-
    import re

    pattern = r"^[a-zA-Z0-9/_+=\.@-]+$"
    return bool(re.match(pattern, name))
