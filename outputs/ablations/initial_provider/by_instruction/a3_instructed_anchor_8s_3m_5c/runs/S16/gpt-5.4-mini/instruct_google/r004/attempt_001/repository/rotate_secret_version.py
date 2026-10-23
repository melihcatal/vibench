from google.cloud import secretmanager

from security_client import build_client, load_config, secret_payload_text, secret_version_path


def rotate_secret_version(secret_id: str = "rotating-secret", version_id: str = "latest") -> str:
    config = load_config(secret_id, version_id)
    client: secretmanager.SecretManagerServiceClient = build_client()
    response = client.access_secret_version(request={"name": secret_version_path(config)})
    return secret_payload_text(response)
