from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


@dataclass
class SecretRequest:
    """Request model for secret operations."""

    secret_name: str
    provider: str
    version: Optional[str] = None
    project_id: Optional[str] = None
    vault_url: Optional[str] = None
    region: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary."""
        result = {"secret_name": self.secret_name, "provider": self.provider}

        if self.version:
            result["version"] = self.version
        if self.project_id:
            result["project_id"] = self.project_id
        if self.vault_url:
            result["vault_url"] = self.vault_url
        if self.region:
            result["region"] = self.region

        return result


@dataclass
class SecretResponse:
    """Response model for secret operations."""

    value: str
    provider: str
    secret_name: str
    version: str
    created_at: str
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_provider_response(
        cls, provider: str, secret_name: str, raw_response: Any
    ) -> "SecretResponse":
        """Create SecretResponse from provider-specific response."""
        if provider == "google":
            from google.cloud.secretmanager import AccessSecretVersionResponse

            if isinstance(raw_response, AccessSecretVersionResponse):
                return cls(
                    value=raw_response.payload.data.decode("UTF-8"),
                    provider=provider,
                    secret_name=secret_name,
                    version=raw_response.name.split("/")[-1],
                    created_at=raw_response.create_time.isoformat(),
                    metadata={"name": raw_response.name},
                )

        elif provider == "azure":
            from azure.keyvault.secrets import KeyVaultSecret

            if isinstance(raw_response, KeyVaultSecret):
                return cls(
                    value=raw_response.value,
                    provider=provider,
                    secret_name=secret_name,
                    version=raw_response.properties.version,
                    created_at=raw_response.properties.created_on.isoformat(),
                    metadata={"id": raw_response.id},
                )

        elif provider == "aws":
            return cls(
                value=raw_response.get("SecretString", ""),
                provider=provider,
                secret_name=secret_name,
                version=raw_response.get("VersionId", ""),
                created_at=raw_response.get("CreatedDate", "").isoformat()
                if raw_response.get("CreatedDate")
                else "",
                metadata={"arn": raw_response.get("ARN")},
            )

        elif provider == "ibm":
            return cls(
                value=raw_response.get("payload", ""),
                provider=provider,
                secret_name=secret_name,
                version=raw_response.get("id", ""),
                created_at=raw_response.get("created_at", ""),
                metadata={"secret_id": raw_response.get("secret_id")},
            )

        # Fallback for unknown provider
        return cls(
            value=str(raw_response),
            provider=provider,
            secret_name=secret_name,
            version="unknown",
            created_at=datetime.now().isoformat(),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        result = {
            "value": self.value,
            "provider": self.provider,
            "secret_name": self.secret_name,
            "version": self.version,
            "created_at": self.created_at,
        }

        if self.metadata:
            result["metadata"] = self.metadata

        return result

    def get_json_value(self) -> Dict[str, Any]:
        """Parse value as JSON if possible."""
        try:
            return json.loads(self.value)
        except json.JSONDecodeError:
            raise ValueError("Secret value is not valid JSON")


@dataclass
class RotationStatus:
    """Model for secret rotation status."""

    secret_name: str
    current_version: str
    previous_version: Optional[str]
    last_rotated: str
    rotation_enabled: bool
    next_rotation: Optional[str]
    provider: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert rotation status to dictionary."""
        result = {
            "secret_name": self.secret_name,
            "current_version": self.current_version,
            "last_rotated": self.last_rotated,
            "rotation_enabled": self.rotation_enabled,
            "provider": self.provider,
        }

        if self.previous_version:
            result["previous_version"] = self.previous_version
        if self.next_rotation:
            result["next_rotation"] = self.next_rotation

        return result
