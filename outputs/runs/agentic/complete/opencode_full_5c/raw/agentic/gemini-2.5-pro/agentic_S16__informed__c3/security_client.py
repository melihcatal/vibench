import os
from google.cloud import secretmanager
from security_models import SecretPayload


def get_secret_manager_client():
    return secretmanager.SecretManagerServiceClient()


def build_secret_name(payload: SecretPayload) -> str:
    return f"projects/{payload.project_id}/secrets/{payload.secret_id}/versions/{payload.version_id}"
