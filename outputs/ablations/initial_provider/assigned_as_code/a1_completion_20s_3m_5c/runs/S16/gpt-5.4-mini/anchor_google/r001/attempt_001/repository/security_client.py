import os

from google.cloud import secretmanager


def load_security_config(config=None):
    config = config or {}
    merged = dict(config)
    merged.setdefault("project_id", os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"))
    merged.setdefault("version", os.getenv("SECRET_VERSION", "latest"))
    merged.setdefault("location", os.getenv("SECRET_LOCATION"))
    return merged


def secret_manager_client():
    return secretmanager.SecretManagerServiceClient()


def secret_name(project_id, secret_id, version="latest"):
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
