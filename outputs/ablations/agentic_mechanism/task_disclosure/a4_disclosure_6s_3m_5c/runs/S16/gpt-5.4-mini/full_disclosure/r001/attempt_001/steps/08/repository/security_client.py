import os
from dataclasses import dataclass


@dataclass(frozen=True)
class SecretManagerConfig:
    project_id: str
    access_token: str
    secret_id: str | None = None
    version: str = "latest"


def _first_env(*names: str) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def load_secret_manager_config(secret_id: str | None = None, version: str | None = None) -> SecretManagerConfig:
    project_id = _first_env("GCP_PROJECT_ID", "GOOGLE_CLOUD_PROJECT", "GCLOUD_PROJECT")
    access_token = _first_env("GCP_ACCESS_TOKEN", "GOOGLE_OAUTH_ACCESS_TOKEN")
    if not project_id:
        raise ValueError("Missing project_id; set GCP_PROJECT_ID, GOOGLE_CLOUD_PROJECT, or GCLOUD_PROJECT")
    if not access_token:
        raise ValueError("Missing access token; set GCP_ACCESS_TOKEN or GOOGLE_OAUTH_ACCESS_TOKEN")
    resolved_secret_id = secret_id or _first_env("GCP_SECRET_ID")
    resolved_version = version or _first_env("GCP_SECRET_VERSION", "GCP_SECRET_STAGE") or "latest"
    return SecretManagerConfig(
        project_id=project_id,
        access_token=access_token,
        secret_id=resolved_secret_id,
        version=resolved_version,
    )


def secret_manager_base_url() -> str:
    return "https://secretmanager.googleapis.com/v1"


def secret_resource_name(project_id: str, secret_id: str, version: str = "latest") -> str:
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version}"


def secret_access_url(project_id: str, secret_id: str, version: str = "latest") -> str:
    return f"{secret_manager_base_url()}/{secret_resource_name(project_id, secret_id, version)}:access"


def secret_access_headers(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}
