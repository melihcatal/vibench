from __future__ import annotations

import os

from google.cloud import secretmanager

from security_models import ParsedSecret, SecretRequest, normalize_secret_name


def default_project_id() -> str:
    project_id = os.getenv("GCP_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError(
            "GCP project id is required via GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT"
        )
    return project_id


def build_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def access_secret(request: SecretRequest) -> ParsedSecret:
    client = build_secret_manager_client()
    name = normalize_secret_name(
        request.project_id, request.secret_id, request.version_id
    )
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    return ParsedSecret(name=name, value=payload, version=request.version_id)


def get_secret_metadata(request: SecretRequest) -> secretmanager.SecretVersion:
    client = build_secret_manager_client()
    name = normalize_secret_name(
        request.project_id, request.secret_id, request.version_id
    )
    return client.get_secret_version(request={"name": name})


def get_secret_resource(
    secret_id: str, project_id: str | None = None
) -> secretmanager.Secret:
    client = build_secret_manager_client()
    resolved_project_id = project_id or default_project_id()
    name = f"projects/{resolved_project_id}/secrets/{secret_id}"
    return client.get_secret(request={"name": name})
