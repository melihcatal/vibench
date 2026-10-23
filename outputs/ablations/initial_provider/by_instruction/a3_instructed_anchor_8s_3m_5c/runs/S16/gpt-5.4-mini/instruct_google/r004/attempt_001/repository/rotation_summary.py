from google.cloud import secretmanager

from security_client import build_client, load_config, secret_version_path


def rotation_summary(secret_id: str = "rotating-secret", version_id: str = "latest") -> str:
    config = load_config(secret_id, version_id)
    client: secretmanager.SecretManagerServiceClient = build_client()
    response = client.access_secret_version(request={"name": secret_version_path(config)})
    return f"{config.secret_id}:{response.name.split('/')[-1]}"
