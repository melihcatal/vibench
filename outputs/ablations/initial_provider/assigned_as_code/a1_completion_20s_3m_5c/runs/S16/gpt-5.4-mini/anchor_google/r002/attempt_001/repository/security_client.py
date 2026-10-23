import os

from google.cloud import secretmanager

from security_models import build_secret_path, get_secret_name, get_version_name


def load_security_config(config=None):
    config = config or {}
    project_id = config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        project_id = os.environ.get("GCP_PROJECT")
    return {"project_id": project_id, "version": config.get("version")}


def create_secret_client():
    return secretmanager.SecretManagerServiceClient()


def fetch_secret_text(payload, config=None):
    config = load_security_config(config)
    client = create_secret_client()
    secret_id = get_secret_name(payload, config)
    version = get_version_name(payload, config)
    name = build_secret_path(config["project_id"], secret_id, version)
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("utf-8")
