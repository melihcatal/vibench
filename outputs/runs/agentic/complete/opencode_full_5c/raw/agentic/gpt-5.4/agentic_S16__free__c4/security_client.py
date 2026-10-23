from __future__ import annotations

import os

from google.cloud import secretmanager
from openai import OpenAI

from security_models import SecretLocator


def get_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_default_locator(secret_id: str, version_id: str = "latest") -> SecretLocator:
    project_id = os.environ["GCP_PROJECT_ID"]
    return SecretLocator(
        project_id=project_id, secret_id=secret_id, version_id=version_id
    )


def access_secret_version(
    locator: SecretLocator,
) -> secretmanager.AccessSecretVersionResponse:
    client = get_secret_manager_client()
    return client.access_secret_version(request={"name": locator.resource_name()})


def get_secret_metadata(secret_id: str) -> secretmanager.Secret:
    client = get_secret_manager_client()
    project_id = os.environ["GCP_PROJECT_ID"]
    name = f"projects/{project_id}/secrets/{secret_id}"
    return client.get_secret(request={"name": name})


def get_secret_version(secret_id: str, version_id: str) -> secretmanager.SecretVersion:
    client = get_secret_manager_client()
    locator = get_default_locator(secret_id=secret_id, version_id=version_id)
    return client.get_secret_version(request={"name": locator.resource_name()})
