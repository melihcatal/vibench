import os
from typing import Any, Optional

from google.cloud import secretmanager

from security_models import SecretRequest, SecretResponse, normalize_secret_text, parse_json_payload


def get_project_id(default: Optional[str] = None) -> str:
    return os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or default or ""


def build_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def access_secret_text(request: SecretRequest, client: Optional[Any] = None) -> SecretResponse:
    client = client or build_client()
    resource = f"projects/{request.project_id}/secrets/{request.secret_name}/versions/{request.version}"
    response = client.access_secret_version(name=resource)
    text = response.payload.data.decode("utf-8")
    return SecretResponse(name=resource, payload=text, raw=response)


def access_secret_json(request: SecretRequest, client: Optional[Any] = None) -> SecretResponse:
    response = access_secret_text(request, client=client)
    return SecretResponse(name=response.name, payload=parse_json_payload(response.payload), raw=response.raw)


def get_secret_value(project_id: str, secret_name: str, version: str = "latest", client: Optional[Any] = None) -> str:
    response = access_secret_text(SecretRequest(project_id=project_id, secret_name=secret_name, version=version), client=client)
    return normalize_secret_text(response.payload)
