from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


@dataclass
class SecretRequest:
    """Request model for secret operations."""

    secret_name: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    metadata_only: bool = False

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
    secret_value: Optional[str] = None
    secret_binary: Optional[bytes] = None
    version_id: Optional[str] = None
    version_stages: List[str] = field(default_factory=list)
    arn: Optional[str] = None
    created_date: Optional[datetime] = None
    last_accessed_date: Optional[datetime] = None
    last_changed_date: Optional[datetime] = None
    tags: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_aws_response(cls, aws_response: Dict[str, Any]) -> "SecretResponse":
        """Create SecretResponse from AWS Secrets Manager response."""
        secret_value = None
        secret_binary = None

        if "SecretString" in aws_response:
            secret_value = aws_response["SecretString"]
        elif "SecretBinary" in aws_response:
            secret_binary = aws_response["SecretBinary"]

        return cls(
            secret_name=aws_response.get("Name", ""),
            secret_value=secret_value,
            secret_binary=secret_binary,
            version_id=aws_response.get("VersionId"),
            version_stages=aws_response.get("VersionStages", []),
            arn=aws_response.get("ARN"),
            created_date=aws_response.get("CreatedDate"),
            last_accessed_date=aws_response.get("LastAccessedDate"),
            last_changed_date=aws_response.get("LastChangedDate"),
            tags={tag["Key"]: tag["Value"] for tag in aws_response.get("Tags", [])},
        )

    def get_value(self) -> Any:
        """Get the secret value as appropriate type."""
        if self.secret_value:
            try:
                return json.loads(self.secret_value)
            except json.JSONDecodeError:
                return self.secret_value
        elif self.secret_binary:
            return self.secret_binary
        return None

    def is_json(self) -> bool:
        """Check if secret value is valid JSON."""
        if not self.secret_value:
            return False
        try:
            json.loads(self.secret_value)
            return True
        except json.JSONDecodeError:
            return False


@dataclass
class SecretMetadata:
    """Metadata model for secret information."""

    name: str
    arn: str
    description: Optional[str] = None
    last_accessed_date: Optional[datetime] = None
    last_changed_date: Optional[datetime] = None
    last_rotated_date: Optional[datetime] = None
    rotation_enabled: bool = False
    rotation_lambda_arn: Optional[str] = None
    rotation_rules: Optional[Dict[str, Any]] = None
    tags: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_aws_describe(cls, aws_response: Dict[str, Any]) -> "SecretMetadata":
        """Create SecretMetadata from AWS describe_secret response."""
        rotation_rules = None
        if "RotationRules" in aws_response:
            rotation_rules = {
                "automatically_after_days": aws_response["RotationRules"].get(
                    "AutomaticallyAfterDays"
                ),
                "duration": aws_response["RotationRules"].get("Duration"),
                "schedule_expression": aws_response["RotationRules"].get(
                    "ScheduleExpression"
                ),
            }

        return cls(
            name=aws_response.get("Name", ""),
            arn=aws_response.get("ARN", ""),
            description=aws_response.get("Description"),
            last_accessed_date=aws_response.get("LastAccessedDate"),
            last_changed_date=aws_response.get("LastChangedDate"),
            last_rotated_date=aws_response.get("LastRotatedDate"),
            rotation_enabled=aws_response.get("RotationEnabled", False),
            rotation_lambda_arn=aws_response.get("RotationLambdaARN"),
            rotation_rules=rotation_rules,
            tags={tag["Key"]: tag["Value"] for tag in aws_response.get("Tags", [])},
        )


@dataclass
class RotationStatus:
    """Model for secret rotation status."""

    secret_name: str
    rotation_enabled: bool
    last_rotation_date: Optional[datetime]
    next_rotation_date: Optional[datetime]
    rotation_interval_days: Optional[int]
    rotation_lambda_arn: Optional[str]
    current_version_id: Optional[str]
    pending_version_id: Optional[str]
    previous_version_id: Optional[str]

    def is_rotation_pending(self) -> bool:
        """Check if rotation is pending."""
        return self.pending_version_id is not None

    def days_since_last_rotation(self) -> Optional[int]:
        """Calculate days since last rotation."""
        from datetime import datetime, timezone

        if not self.last_rotation_date:
            return None

        now = datetime.now(timezone.utc)
        delta = now - self.last_rotation_date
        return delta.days


@dataclass
class ValidationResult:
    """Model for validation results."""

    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, error: str) -> None:
        """Add an error message."""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str) -> None:
        """Add a warning message."""
        self.warnings.append(warning)
