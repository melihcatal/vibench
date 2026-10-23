import os

from google.cloud import secretmanager


def load_config(config=None):
    config = config or {}
    merged = {
        "project_id": config.get("project_id") or os.environ.get("GCP_PROJECT_ID") or os.environ.get("GOOGLE_CLOUD_PROJECT"),
        "version": config.get("version") or os.environ.get("SECRET_VERSION", "latest"),
        "secret_id": config.get("secret_id"),
        "stage": config.get("stage") or os.environ.get("SECRET_STAGE", "latest"),
    }
    return merged


def get_client():
    return secretmanager.SecretManagerServiceClient()


def secret_name(project_id, secret_id, version):
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version}"


def decode_payload(response):
    return response.payload.data.decode("utf-8")
