import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

from google.cloud import secretmanager


@dataclass(frozen=True)
class RotationSummary:
    secret_id: str
    version_name: str
    state: str
    enabled: bool
    created_at: Optional[str]
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "secret_id": self.secret_id,
            "version_name": self.version_name,
            "state": self.state,
            "enabled": self.enabled,
            "created_at": self.created_at,
            "summary": self.summary,
        }


def _client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def _project_id() -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
    return project_id


def _secret_name(project_id: str, secret_id: str) -> str:
    return f"projects/{project_id}/secrets/{secret_id}"


def _format_timestamp(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    text = str(value).strip()
    return text or None


def summarize_secret_rotation(secret_id: str, version: str = "latest") -> RotationSummary:
    project_id = _project_id()
    client = _client()
    version_name = f"{_secret_name(project_id, secret_id)}/versions/{version}"
    secret_version = client.access_secret_version(request={"name": version_name})
    version_info = secret_version.name or version_name
    state = secret_version.name.split("/")[-2] if "/versions/" in secret_version.name else "UNKNOWN"
    enabled = state.upper() == "ENABLED"
    created_at = _format_timestamp(getattr(secret_version, "create_time", None))
    summary = f"{secret_id} version {version_info} is {state.lower()}"
    if created_at:
        summary += f" and was created at {created_at}"
    return RotationSummary(
        secret_id=secret_id,
        version_name=version_info,
        state=state,
        enabled=enabled,
        created_at=created_at,
        summary=summary,
    )
