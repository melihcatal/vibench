"""
Local request, response, and normalization helpers for Secret Management.
Defines data classes and utility functions for working with secret data.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List


@dataclass
class SecretRequest:
    """Request parameters for secret operations."""

    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    metadata_only: bool = False
    include_labels: bool = False


@dataclass
class SecretResponse:
    """Standardized response from secret retrieval operations."""

    success: bool = False
    secret_id: str = ""
    secret_value: Optional[str] = None
    secret_binary: Optional[bytes] = None
    version_id: Optional[str] = None
    version_stage: List[str] = field(default_factory=list)
    arn: Optional[str] = None
    created_date: Optional[datetime] = None
    last_changed_date: Optional[datetime] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

    @property
    def is_error(self) -> bool:
        return not self.success

    @property
    def secret_string(self) -> Optional[str]:
        return self.secret_value

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "success": self.success,
            "secret_id": self.secret_id,
            "version_id": self.version_id,
            "version_stage": self.version_stage,
            "arn": self.arn,
            "error_code": self.error_code,
            "error_message": self.error_message,
        }
        if self.secret_value is not None:
            result["secret_value"] = self.secret_value
        if self.created_date:
            result["created_date"] = self.created_date.isoformat()
        if self.last_changed_date:
            result["last_changed_date"] = self.last_changed_date.isoformat()
        return result


@dataclass
class ParsedSecret:
    """Represents a parsed secret with metadata."""

    secret_id: str
    raw_value: str
    parsed_data: Dict[str, Any] = field(default_factory=dict)
    parse_format: str = "unknown"
    is_valid: bool = False
    parse_error: Optional[str] = None

    def get_nested_value(self, key_path: str, default: Any = None) -> Any:
        """Retrieve a nested value from parsed secret data using dot notation."""
        keys = key_path.split(".")
        current = self.parsed_data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current


@dataclass
class RotationStatus:
    """Tracks rotation status for a secret."""

    secret_id: str
    is_rotating: bool = False
    last_rotated: Optional[datetime] = None
    next_rotation: Optional[datetime] = None
    rotation_lambda_arn: Optional[str] = None
    rotation_rules: Optional[Dict[str, Any]] = None
    current_version_id: Optional[str] = None
    pending_version_id: Optional[str] = None
    version_stages: Dict[str, List[str]] = field(default_factory=dict)

    def to_summary(self) -> Dict[str, Any]:
        return {
            "secret_id": self.secret_id,
            "is_rotating": self.is_rotating,
            "last_rotated": self.last_rotated.isoformat() if self.last_rotated else None,
            "next_rotation": self.next_rotation.isoformat() if self.next_rotation else None,
            "current_version_id": self.current_version_id,
            "pending_version_id": self.pending_version_id,
            "rotation_lambda": self.rotation_lambda_arn,
            "version_stages": self.version_stages,
        }


@dataclass
class SecretLabel:
    """Represents a label or note attached to a secret."""

    secret_id: str
    label_text: str
    label_type: str = "note"
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    is_unsafe: bool = False
    safety_flags: List[str] = field(default_factory=list)


def parse_secret_json(raw_value: str) -> ParsedSecret:
    """
    Parse a JSON-formatted secret value.

    Args:
        raw_value: Raw string value of the secret.

    Returns:
        ParsedSecret with parsed data and validation status.
    """
    try:
        parsed = json.loads(raw_value)
        return ParsedSecret(
            raw_value=raw_value,
            parsed_data=parsed,
            parse_format="json",
            is_valid=True,
        )
    except json.JSONDecodeError as e:
        return ParsedSecret(
            raw_value=raw_value,
            parse_format="json",
            is_valid=False,
            parse_error=str(e),
        )


def normalize_aws_response_to_secret_response(aws_response: Dict[str, Any]) -> SecretResponse:
    """
    Convert an AWS Secrets Manager response dict to a SecretResponse.

    Args:
        aws_response: Raw response from AWS Secrets Manager.

    Returns:
        Normalized SecretResponse object.
    """
    response = SecretResponse(
        success=True,
        secret_id=aws_response.get("Name", ""),
        version_id=aws_response.get("VersionId", ""),
        version_stage=aws_response.get("VersionStage", []),
        arn=aws_response.get("ARN", ""),
        created_date=aws_response.get("CreatedDate"),
        last_changed_date=aws_response.get("LastChangedDate"),
        raw_response=aws_response,
    )

    if "SecretString" in aws_response:
        response.secret_value = aws_response["SecretString"]
    elif "SecretBinary" in aws_response:
        response.secret_binary = aws_response["SecretBinary"]

    return response


def build_error_secret_response(error_code: str, error_message: str, secret_id: str = "") -> SecretResponse:
    """
    Build a SecretResponse representing an error condition.

    Args:
        error_code: AWS error code.
        error_message: Error description.
        secret_id: Optional secret identifier.

    Returns:
        SecretResponse with error details.
    """
    return SecretResponse(
        success=False,
        secret_id=secret_id,
        error_code=error_code,
        error_message=error_message,
    )
